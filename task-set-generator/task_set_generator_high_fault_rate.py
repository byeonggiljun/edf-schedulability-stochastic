import argparse
from dataclasses import dataclass
import logging
import math
import random
import pandas as pd
import sys

CUSTOM_LEVEL = 15
logging.addLevelName(CUSTOM_LEVEL, "VERBOSE")

def verbose(self, message, *args, **kwargs):
  if self.isEnabledFor(CUSTOM_LEVEL):
    self._log(CUSTOM_LEVEL, message, args, **kwargs)

logging.Logger.verbose = verbose

logger = logging.getLogger(__name__)

@dataclass
class Task:
  id: int
  execution_time: int
  period: int
  due_portion: float
  sdc_portion: float
  fr_min: float

time_unit = 1e-4 # Time unit is 100 us.
# time_unit = 0.001 # Time unit is 1 ms.
# time_unit = 1 # Time unit is 1 s.
k = 60 / time_unit

p_due_unit = 0
p_benign_unit = 0

required_failure_rates_hours = [1e-3, 1e-5, 1e-7, 1e-9]
required_failure_rates = [1 - (1 - rate) ** (1/k) for rate in required_failure_rates_hours] # rate per min
due_sdc_rates = [[0.264, 0.019], [0.268, 0.037], [0.224, 0.019], [0.279, 0.019], [0.266, 0.028], [0.296, 0.009], [0.255, 0.019]]

def uunifast(n, u):
  utilizations = []
  sum_u = u

  for i in range(1, n):
    next_sum_u = sum_u * (random.random() ** (1 / (n - i)))
    utilizations.append(sum_u - next_sum_u)
    sum_u = next_sum_u
    
  utilizations.append(sum_u)
  logger.debug(utilizations)
  return utilizations

def find_max_reexec_Reghenzani(task, lb):
  p_unit = 1 - ((1 - lb) ** (1 / k)) # Eq 4
  max_reexec_Reghenzani = 0
  while True:
    p_fault_exec = 1 - (1 - p_unit) ** (task.execution_time) # Eq 1
    p_fault_reexec = p_fault_exec ** (1 + max_reexec_Reghenzani) # Eq 3

    fr_exec = 1 - ((1 - task.fr_min) ** (task.period / k))

    if p_fault_reexec < fr_exec:
      return max_reexec_Reghenzani, p_fault_reexec
    max_reexec_Reghenzani += 1

# def compute_p_fault_Reghenzani(task, lb, max_reexec_Reghenzani):
#   p_unit = 1 - ((1 - lb) ** (1 / k)) # Eq 4
#   p_fault_exec = 1 - (1 - p_unit) ** (task.execution_time) # Eq 1
#   p_fault_reexec = p_fault_exec ** (1 + max_reexec_Reghenzani) # Eq 3

#   return p_fault_reexec

def find_max_reexec_RTailor(task, lb):
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
  max_reexec_RTailor = 0
  while True:
    p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9
    p_due_reexec = p_due_exec ** (1 + max_reexec_RTailor) # Eq 12

    fr_exec = 1 - ((1 - task.fr_min) ** (task.period / k))

    if p_due_reexec < fr_exec:
      return max_reexec_RTailor, p_due_reexec
    max_reexec_RTailor += 1

def compute_p_due_reexec(task, lb, max_reexec_RTailor):
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6

  p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9
  p_due_reexec = p_due_exec ** (1 + max_reexec_RTailor) # Eq 12

  return p_due_reexec

def compute_p_sdc(task, lb, max_reexec, max_proact):
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
  p_sdc_unit = 1 - ((1 - lb * task.sdc_portion) ** (1 / k)) # Eq 7
  p_benign_unit = 1 - p_due_unit - p_sdc_unit # Eq 8
  
  p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9
  p_benign_exec = p_benign_unit ** task.execution_time # 11
  p_sdc_exec = 1 - (p_benign_exec + p_due_exec)

  p_sdc_reexec = 0
  for m in range(1, max_proact + 1): # from 1 to max_proact
    p_completed_m = 0
    if m < max_proact:
      p_completed_m = math.comb((1 + max_reexec), m) * (p_due_exec ** (max_reexec + 1 - m)) * ((1 - p_due_exec) ** m) #Eq 14-1
    elif m == max_proact:
      for n in range(m, 2 + max_reexec): # from M to 1 + N
        p_completed_m += math.comb(n - 1, m - 1) * (p_due_exec ** (n - m)) * ((1 - p_due_exec) ** m) # Eq 14-2

    p_sdc_m = 0
    for m_sdc in range(math.ceil(m / 2), m + 1): # From the ceiling of m /2 to m
      p1 = p_sdc_exec / (p_sdc_exec + p_benign_exec)
      p2 = p_benign_exec / (p_sdc_exec + p_benign_exec)
      p_sdc_m += math.comb(m, m_sdc) * (p1 ** m_sdc) * (p2 ** (m - m_sdc)) # Eq 15
    p_sdc_reexec += p_completed_m * p_sdc_m # Eq 13
  return p_sdc_reexec

def find_max_proactive(task, lb, max_reexec):
  for max_proact_cand in range(1, max_reexec + 2, 2):
    p_sdc_reexec = compute_p_sdc(task, lb, max_reexec, max_proact_cand)
    if p_sdc_reexec < task.fr_min:
      return max_proact_cand
  return -1

def generate_task_set(n, lb, u):

  tasks = []
  output = []
  while True:
    utilizations = uunifast(n, u)
    # utilizations = [0.05, 0.1, 0.05, 0.1, 0.3]

    zero_detected = False
    for i in range(0, n):
      # Assign a random period.
      # period = random.randint(50, 1000)
      period = random.randint(500, 10000)

      max_reexec_RTailor = 0
      already_found_RTailor = False
      for max_reexec_cand in range (0, 10):
        execution_time = math.floor(utilizations[i] * period / (1 + max_reexec_cand))
        if execution_time == 0:
          zero_detected = True
          break
        fr_index = random.randint(0, len(required_failure_rates) -1)
        fr_min = required_failure_rates[fr_index] # Allocate a required failure rate.
        due_portion, sdc_portion = due_sdc_rates[random.randint(0, len(due_sdc_rates) - 1)]
        
        new_task = Task(id=i, execution_time=execution_time, period=period, due_portion=due_portion, sdc_portion=sdc_portion, fr_min=fr_min)
        p_due_reexec = compute_p_due_reexec(new_task, lb, max_reexec_cand)

        fr_exec = 1 - ((1 - new_task.fr_min) ** (new_task.period / k))
        if p_due_reexec < fr_exec:
          if not already_found_RTailor:
            max_reexec_RTailor = max_reexec_cand
          max_proact_cand = find_max_proactive(new_task, lb, max_reexec_cand)
          if max_proact_cand == -1:
            continue
          else:
            tasks.append(new_task)
            output.append([new_task.id, new_task.execution_time, new_task.period, new_task.due_portion, new_task.sdc_portion, new_task.fr_min, required_failure_rates_hours[fr_index], max_reexec_RTailor, max_reexec_cand, max_proact_cand])
            break

      if zero_detected:
        break
    if zero_detected:
      logger.debug("Zero detected.")
      tasks = []
    else:
      break
  
  df = pd.DataFrame(output, columns=['id', 'ET', 'Period', 'DUE', 'SDC', 'RequiredFailureRate', 'RequiredRateHour', 'N_RTailor', 'N', 'M'])
  df.to_csv('output_test.csv', index=False)

def main_loop(n, lb, u):
  generate_task_set(n, lb, u)

def main():
  global logger
  global p_due_unit, p_benign_unit
  parser = argparse.ArgumentParser(description="Schedulability test with EDF scheduler")
  parser.add_argument('-d', '--debug', action='store_true', help="Debug mode")
  parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")
  parser.add_argument('-t', '--test', action='store_true', help="Test")

  # Parse arguments
  args = parser.parse_args()

  if args.debug:
    print("Debug Mode.")
    logging.basicConfig(level=logging.DEBUG)
  if args.verbose:
    print("Verbose Mode.")
    logging.basicConfig(level=CUSTOM_LEVEL)
    logger = logging.getLogger(__name__)
  if args.test is not None:
    # To test only 1 task, put 1 as the first argument.
    # Number of tasks, fault rate, total utilization.
    # generate_task_set(5, 1e-2, 0.25)
    main_loop(10, 1e-2, 0.5)
    exit()

  # Make tuples of (n, NU, Lambda)
  for n in [5, 10, 25, 50]:
    for lb in [1e-2, 1e-3, 1e-4, 1e-5]:
      # for u in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
      for u in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        main_loop(n, lb, u)
        
if __name__ == "__main__":
  main()