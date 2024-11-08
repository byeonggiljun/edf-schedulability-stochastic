import argparse
import logging
import os
import pandas as pd
import random
import sys
from dataclasses import dataclass

CUSTOM_LEVEL = 15
logging.addLevelName(CUSTOM_LEVEL, "VERBOSE")

def verbose(self, message, *args, **kwargs):
  if self.isEnabledFor(CUSTOM_LEVEL):
    self._log(CUSTOM_LEVEL, message, args, **kwargs)

logging.Logger.verbose = verbose

logger = logging.getLogger(__name__)

timeout = 0 # Total Execution Time
current_time = 0 # Current time
task_set_info = [] # Input task set
tasks = []
output = []

max_reexec = 0
min_success = 0

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
def has_failed(p):
  fail = 1 if random.random() < p else 0
  return fail

def is_finished(task):
  return 1

def initialize_tasks():
  for task_info in task_set_info:
    # Deadline, Arrival Time, remaining execution time, id
    task = Task(id=task_info[0], deadline=task_info[2], arrival_time=0,
                remaining_exec_time=task_info[1], num_reexec=0, num_success=0)
    tasks.append(task)
    output.append([current_time, 'schedule', task.id, task.arrival_time,
                task.remaining_exec_time, task.deadline, -1, 0, 0])

def execute_task(task, until):
  global current_time
  execution_time = until - current_time
  logger.verbose(f"Execute {execution_time}.")
  if execution_time < 0:
    sys.exit("Error: the time tries to go back.")
  elif execution_time == 0:
    # TODO: Is this an error?
    print(f"Warning: The task is peeked {task.id} but the execution time is 0.")
  task.remaining_exec_time = task.remaining_exec_time - execution_time
  current_time = until

# Reschedule a task.
def reschedule_task(task, has_failed=False):
  id = task.id
  task.remaining_exec_time = task_set_info[id][1] # Execution time
  if has_failed:
    if task.num_reexec < max_reexec:
      # The number of reexecution does not exceed the boundary.
      if current_time < task.deadline:
        logger.verbose(f"Reschedule the task {task.id} cause it has failed.")
        # Can schedule the same task again.
        # TODO: Check max_reexec
        task.arrival_time = current_time
        task.num_reexec += 1
        output.append([current_time, 'reschedule', id, task.arrival_time,
                    task.remaining_exec_time, task.deadline, -1, task.num_reexec, task.num_success])
        return
      elif current_time == task.deadline:
        # Can't schedule the task again (automatically drop it). Instead, schedule the next task.
        logger.debug(f"Current time {current_time} is identical to the deadline {task.deadline}. Can't re-execute.")
        task.num_reexec += 1
        output.append([current_time, 'drop(violation)', id, current_time,
                        task.remaining_exec_time, task.deadline, -1, task.num_reexec, task.num_success])
      else: # current time > task.deadline
        sys.exit(f"Error: Current time {current_time} exceeds the deadline {task.deadline}. This must already be handled.")
    else:
      # Can't reschedule cause we already re-execute this task with the max allowed time.
      logger.verbose(f"Can't reschedule. num_reexec {task.num_reexec} is already {max_reexec}")
      output.append([current_time, 'drop(overrun)', id, task.arrival_time,
                      0, task.deadline, -1, task.num_reexec, task.num_success])

  # Schedule the next task.
  task.num_reexec = 0
  task.arrival_time = task.deadline
  task.deadline = task.arrival_time + task_set_info[id][2] # Arrival time + Period

  output.append([current_time, 'schedule', id, task.arrival_time,
                  task.remaining_exec_time, task.deadline, -1, task.num_reexec, task.num_success])


def edf_schedulability_test():
  global current_time
  while current_time < timeout:
    tasks_not_ready = []
    min_deadline_ready = sys.maxsize
    task_to_process = None
    for task in tasks:
      if task.arrival_time <= current_time:
        if task.deadline < min_deadline_ready:
          # print(f"task {task.id}, arrival_time = {task.arrival_time}, current_time = {current_time}")
          task_to_process = task
          min_deadline_ready = task.deadline
      else:
        tasks_not_ready.append(task)
    
    tasks_not_ready.sort(key=return_arrival_time)

    if task_to_process == None:
      # No task to execute at this time. Advance to the earliest task's arrival time or timeout time.
      output.append([current_time, 'IDLE', -1, -1, -1, -1, -1, -1, -1])
      current_time = min(tasks_not_ready[0].arrival_time, timeout)
    else:
      logger.verbose(f"ID of the task to process is {task_to_process.id}")
      output.append([current_time, 'run', task_to_process.id, task_to_process.arrival_time,
                     task_to_process.remaining_exec_time, task_to_process.deadline, -1, task.num_reexec, task.num_success])
      
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
        logger.verbose(f"No preemption happens during the task {task_to_process.id}'s execution time")
        # Compare the expected finish time, deadline, and timeout.
        expected_finish_time = current_time + task_to_process.remaining_exec_time
        time_to_advance = min(expected_finish_time, task_to_process.deadline, timeout)

        if time_to_advance == expected_finish_time:
          # Normal case. No violation.
          # Finish the current task
          execute_task(task_to_process, expected_finish_time)

          # TODO: Check whether the task has failed. If it has failed, rescheudle it.
          fail = False
          if has_failed(task_set_info[task_to_process.id][3]):
            print(f"The test has failed with the proability {task_set_info[task_to_process.id][3]}")
            fail = True
          output.append([current_time, 'success', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, fail, 
                         task.num_reexec, task.num_success])
          # TODO: Check min_success
          # Schedule the next task
          reschedule_task(task_to_process, fail)
        elif time_to_advance == task_to_process.deadline:
          # Deadline violation occurs before the preemption happens.
          # Run the current task until the deadline, drop it, and find the new task to execute.
          execute_task(task_to_process, task_to_process.deadline)
          output.append([current_time, 'drop(violation)', task_to_process.id, task_to_process.arrival_time,
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                        task.num_reexec,task.num_success])

          # Reschedule the task
          reschedule_task(task_to_process)
        else:
          # Timeout occurs before finishing this task
          execute_task(task_to_process, timeout)
          output.append([current_time, 'exit(timeout)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                        task.num_reexec, task.num_success])
      else:
        # The task task_to_preempt will preempt this task.
        # Compare the preemption time, deadline, and timeout.
        time_to_advance = min(task_to_preempt.arrival_time, task_to_process.deadline, timeout)

        if time_to_advance == task_to_preempt.arrival_time:
          # Normal case. Just run the current task and preempt.
          execute_task(task_to_process, task_to_preempt.arrival_time)

          logger.verbose(f"At {task_to_preempt.arrival_time}, preemption occurs")
          output.append([current_time, 'pause', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                         task.num_reexec, task.num_success])
        elif time_to_advance == task_to_process.deadline:
          # Deadline violation occurs before the preemption happens.
          # Run the current task until the deadline, drop and reschedule the current task.
          execute_task(task_to_process, task_to_process.deadline)
          output.append([current_time, 'drop(violation)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                        task.num_reexec, task.num_success])

          # Reschedule the task
          reschedule_task(task_to_process)
          output.append([current_time, 'schedule', task_to_process.id, task_to_process.arrival_time,
                         task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                         task.num_reexec, task.num_success])
        else:
          # Timeout occurs before the preemption happens.
          execute_task(task_to_process, timeout)
          output.append([current_time, 'exit(timeout)', task_to_process.id, task_to_process.arrival_time, 
                        task_to_process.remaining_exec_time, task_to_process.deadline, -1,
                        task.num_reexec, task.num_success])

    logger.verbose(f"Advance the current time to {current_time}")
    if logging.getLogger().isEnabledFor(logging.DEBUG):
      print_list(tasks)
    if current_time == timeout:
      logger.debug("Timeout occurs")
      output.append([current_time, 'timeout', -1, -1, -1, -1, -1, -1, -1])
    elif current_time > timeout:
      # sys.exit("Error: the current time exceeds the timeout time.")
      print("Exceed")

def print_list(list):
  for element in list:
    print(element)

def main():
  global timeout
  global task_set_info
  global logger
  global max_reexec
  global min_success
  parser = argparse.ArgumentParser(description="Schedulability test with EDF scheduler")
  parser.add_argument('input_file', type=str, help="The input CSV file name")
  parser.add_argument('-d', '--debug', action='store_true', help="Debug mode")
  parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")
  parser.add_argument('-t', '--timeout', type=int, nargs=1, help="Total Execution time")
  parser.add_argument('-n', '--nmax', type=int, nargs=1, help="Maximum allowed reexecution time")
  parser.add_argument('-m', '--min', type=int, nargs=1, help="Minimum required successive non-failure execution")
  
  # Parse arguments
  args = parser.parse_args()

  readCSV(args.input_file)
  if args.debug:
    print("Debug Mode.")
    logging.basicConfig(level=logging.DEBUG)
  if args.verbose:
    print("Verbose Mode.")
    logging.basicConfig(level=CUSTOM_LEVEL)
    logger = logging.getLogger(__name__)
  if args.timeout is not None:
    timeout = args.timeout[0]
  if args.nmax is not None:
    max_reexec = args.nmax[0]
  if args.min is not None:
    min_success = args.min[0]
  
  print(f"Total Execution Time: {timeout}")
  print(f"Maximum allowed reexecution time (N): {max_reexec}")
  print(f"Minimum required successive non-failure execution time (M): {min_success}")

  initialize_tasks()
  logger.debug("Initial task sets")
  if logging.getLogger().isEnabledFor(logging.DEBUG):
    print_list(tasks)

  edf_schedulability_test()
  
  base_name =os.path.splitext(args.input_file)[0]
  output_file = f"output_{base_name}.csv"
  df = pd.DataFrame(output, columns=['Time', 'Action', 'ID', 'ArrivalTime', 'RemainingExecutionTime', 'Deadline', 'Failed', 'NumReExec', 'NumSuccess'])
  df.to_csv(output_file, index=False)

if __name__ == "__main__":
  main()