import argparse
import logging
import os
import pandas as pd
import random
import sys
from dataclasses import dataclass

timeout = 0 # Total Execution Time
current_time = 0 # Current time
task_set_info = [] # Input task set
tasks = []
output = []

@dataclass
class Task:
  id: int
  deadline: int
  arrival_time: int
  remaining_exec_time: int
  num_reexec: int
  num_success: int

# Read CSV file and store the tasks
def readCSV(input_file):
  global task_set_info
  if not input_file.endswith('.csv'):
    sys.exit("Please provide a CSV file.")

  if not os.path.isfile(input_file):
    sys.exit(f"No file named {input_file}.")

  try:
    df = pd.read_csv(input_file)
    # task_set_info = df.values.tolist()
    task_set_info = [[int(row[0]), int(row[1]), int(row[2]), float(row[3])] for row in df.values]
    if len(task_set_info) == 0:
        sys.exit("No task to process.")
  except Exception as e:
    print(f"Reading the file {input_file} failed with error {e}")

def return_arrival_time(task):
  return task.arrival_time

# Check whether the task has failed or not.
# This function returns 1 with probability p.
def is_failed(p):
  fail = 1 if random.random() < p else 0
  return fail

def initialize_tasks():
  for task_info in task_set_info:
    # Deadline, Arrival Time, remaining execution time, id
    task = Task(id=task_info[0], deadline=task_info[2], arrival_time=0,
                remaining_exec_time=task_info[1], num_reexec=0, num_success=0)
    tasks.append(task)

def execute_task(task, until):
  global current_time
  execution_time = until - current_time
  if execution_time < 0:
    sys.exit("Error: the time tries to go back.")
  elif execution_time == 0:
    # TODO: Is this an error?
    print(f"Warning: The task is peeked {task.id} but the execution time is 0.")
  task.remaining_exec_time = task.remaining_exec_time - execution_time
  current_time = until

# Reschedule a task.
def reschedule_task(task):
  id = task.id
  task.arrival_time = task.deadline
  task.deadline = task.arrival_time + task_set_info[id][2] # Arrival time + Period
  task.remaining_exec_time = task_set_info[id][1] # Execution time


def edf_schedulability_test():
  global current_time
  while current_time < timeout:
    time_to_advance = 0
    tasks_not_ready = []
    min_deadline_ready = sys.maxsize
    task_to_process = None
    for task in tasks:
      if task.arrival_time <= current_time:
        if task.deadline < min_deadline_ready:
          task_to_process = task
          min_deadline_ready = task.deadline
      else:
        tasks_not_ready.append(task)
    
    tasks_not_ready.sort(key=return_arrival_time)

    if task_to_process == None:
      # No task to execute at this time. Advance to the earliest task's arrival time.
      time_to_advance = tasks_not_ready[0].arrival_time - current_time
      current_time += time_to_advance
      output.append([current_time, 'IDLE', -1, -1, -1, -1, -1])
    else:
      logging.debug(f"ID of the task to process is {task_to_process.id}")
      output.append([current_time, 'run', task_to_process.id, task_to_process.arrival_time, task_to_process.remaining_exec_time, task_to_process.deadline, -1])
      
      # Check whether this task would be preempted.
      task_to_preempt = task_to_process
      for task in tasks_not_ready:
        if (task.deadline < task_to_process.deadline and 
          task.arrival_time < current_time + task_to_process.remaining_exec_time):
          # Among tasks sorted by their arriving time, this task has a higher priority than the task to process.
          # Also, this task will be arriving before finishing the task to process. 
          task_to_preempt = task
          break
      
      if (task_to_process.id == task_to_preempt.id):
        # There is no task to preempt task_to_process.
        logging.debug(f"No preemption happens during the task {task_to_process.id}'s execution time")
        # Compare the expected finish time, deadline, and timeout.
        expected_finish_time = current_time + task_to_process.remaining_exec_time
        time_to_advance = min(expected_finish_time, task_to_process.deadline, timeout)

        if time_to_advance == expected_finish_time:
          # Normal case. No violation.
          # Finish the current task
          execute_task(task_to_process, expected_finish_time)

          # TODO: Check whether the task has failed. If it has failed, rescheudle it.
          output.append([current_time, 'finish', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, 0])

          # Schedule the next task
          reschedule_task(task_to_process)
          output.append([current_time, 'schedule', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1])
        elif time_to_advance == task_to_process.deadline:
          # Deadline violation occurs before the preemption happens.
          # Run the current task until the deadline, drop it, and find the new task to execute.
          execute_task(task_to_process, task_to_process.deadline)
          output.append([current_time, 'drop(violation)', task_to_process.id, task_to_process.arrival_time,
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1])

          # Reschedule the task
          reschedule_task(task_to_process)
          output.append([current_time, 'schedule', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1])
        else:
          # Timeout occurs before finishing this task
          execute_task(task_to_process, timeout)
          output.append([current_time, 'exit(timeout)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1])
      else:
        # The task task_to_preempt will preempt this task.
        # Compare the preemption time, deadline, and timeout.
        time_to_advance = min(task_to_preempt.arrival_time, task_to_process.deadline, timeout)

        if time_to_advance == task_to_preempt.arrival_time:
          # Normal case. Just run the current task and preempt.
          execute_task(task_to_process, task_to_preempt.arrival_time)

          logging.debug(f"At {task_to_preempt.arrival_time}, preemption occurs")
          output.append([current_time, 'pause', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1])
        elif time_to_advance == task_to_process.deadline:
          # Deadline violation occurs before the preemption happens.
          # Run the current task until the deadline, drop and reschedule the current task.
          execute_task(task_to_process, task_to_process.deadline)
          output.append([current_time, 'drop(violation)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1])

          # Reschedule the task
          reschedule_task(task_to_process)
          output.append([current_time, 'schedule', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1])
        else:
          # Timeout occurs before the preemption happens.
          execute_task(task_to_process, timeout)
          output.append([current_time, 'exit(timeout)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1])

    logging.debug(f"Advance the current time to {current_time}")
    if logging.getLogger().isEnabledFor(logging.DEBUG):
      print_list(tasks)
    if current_time == timeout:
      logging.debug("Timeout occurs")
      output.append([current_time, 'timeout', -1, -1, -1, -1, -1])
    elif current_time > timeout:
      sys.exit("Error: the current time exceeds the timeout time.")

def print_list(list):
  for element in list:
    print(element)

def main():
  global timeout
  global task_set_info
  parser = argparse.ArgumentParser(description="Schedulability test with EDF scheduler")
  parser.add_argument('input_file', type=str, help="The input CSV file name")
  parser.add_argument('-t', '--timeout', type=int, nargs=1, help="Total Execution time")
  parser.add_argument('-d', '--debug', action='store_true', help="Debug mode")
  
  # Parse arguments
  args = parser.parse_args()

  readCSV(args.input_file)
  if args.timeout is not None:
    timeout = args.timeout[0]
    print(f"Total Execution Time: {timeout}")
  if args.debug:
    print("Debug Mode.")
    logging.basicConfig(level=logging.DEBUG)

  initialize_tasks()
  logging.debug("Initial task sets")
  if logging.getLogger().isEnabledFor(logging.DEBUG):
    print_list(tasks)

  edf_schedulability_test()
  
  base_name =os.path.splitext(args.input_file)[0]
  output_file = f"output_{base_name}.csv"
  df = pd.DataFrame(output, columns=['Time', 'Action', 'ID', 'ArrivalTime', 'RemainingExecutionTime', 'Deadline', 'Failed'])
  df.to_csv(output_file, index=False)

if __name__ == "__main__":
  main()