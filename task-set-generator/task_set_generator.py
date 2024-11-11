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
  fr_hour: float

# time_unit = 1e-6 # Time unit is 1 us.
time_unit = 0.001 # Time unit is 1 ms.
# time_unit = 1 # Time unit is 1 s.
k = 3600 / time_unit

due_portion = 0.25
sdc_portion = 0.002

p_due_unit = 0
p_benign_unit = 0

required_failure_rates = [1e-3, 1e-5, 1e-7, 1e-9]

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

def generate_task_set(n, lb, u):
  p_due_unit = 1 - ((1 - lb * due_portion) ** (1 / k)) # Eq 6
  p_unit = 1 - ((1 - lb) ** (1 / k)) # Eq 4
  p_sdc_unit = 1 - ((1 - lb * sdc_portion) ** (1 / k)) # Eq 7
  p_benign_unit = 1 - p_due_unit - p_sdc_unit # Eq 8

  def find_max_reexec_Reghenzani(task):
    max_reexec_Reghenzani = 0
    while True:
      p_fault_exec = 1 - (1 - p_unit) ** (task.execution_time) # Eq 1
      p_fault_re_exec = p_fault_exec ** (1 + max_reexec_Reghenzani) # Eq 3

      fr_exec = 1 - ((1 - task.fr_hour) ** (task.period / k))

      if p_fault_re_exec < fr_exec:
        return max_reexec_Reghenzani, p_fault_re_exec
      max_reexec_Reghenzani += 1

  def find_max_reexec_RTailor(task):
    max_reexec_RTailor = 0
    while True:
      p_due_exec = 1 - (1 - p_due_unit) ** (execution_time) # Eq 9
      p_due_re_exec = p_due_exec ** (1 + max_reexec_RTailor) # Eq 12

      fr_exec = 1 - ((1 - task.fr_hour) ** (task.period / k))

      if p_due_re_exec < fr_exec:
        return max_reexec_RTailor, p_due_re_exec
      max_reexec_RTailor += 1
  
  def compute_p_sdc(task, max_reexec, max_proact):
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

  tasks = []
  while True:
    utilizations = uunifast(n, u)
    # utilizations = [0.05, 0.1, 0.05, 0.1, 0.3]

    zero_detected = False
    for i in range(0, n):
      # Assign a random period.
      period = random.randint(50, 1000)
      # period = random.randint(5e4, 1e6)
      execution_time = math.floor(utilizations[i] * period / (1 + 2)) # Assume max_reexec is less than 3
      if execution_time == 0:
        zero_detected = True
        break
      fr_hour = required_failure_rates[random.randint(0, 3)] # Allocate a required failure rate.
      tasks.append(Task(id=i, execution_time=execution_time, period=period, fr_hour=fr_hour))
    if zero_detected:
      print("Zero detected.")
      tasks = []
    else:
      break

  # Now we have tasks. Let's compute N and M using P_due and P_sdc.
  output = []
  for task in tasks:
    fr_exec = 1 - ((1 - task.fr_hour) ** (task.period / k))

    max_reexec_Reghenzani, p_fault_re_exec = find_max_reexec_Reghenzani(task)
    max_reexec_RTailor, p_due_re_exec = find_max_reexec_RTailor(task)

    if max_reexec_Reghenzani > 2 or max_reexec_RTailor > 2:
      sys.exit("N larger than 3 found.")

    # p_sdc_Reghenzani = compute_p_sdc(task, max_reexec_Reghenzani, 1)
    p_sdc_RTailor = compute_p_sdc(task, max_reexec_RTailor, 1)

    # p_actual_failure_Reghenzani = p_fault_re_exec + p_sdc_Reghenzani
    p_actual_failure_RTailor = p_due_re_exec + p_sdc_RTailor

    # does_Reghenzani_satisfy = p_actual_failure_Reghenzani < fr_exec
    does_RTailor_satisfy = p_actual_failure_RTailor < fr_exec

    if not does_RTailor_satisfy:
      # N is 0, 1, or 2.
      # Check with (N, M) = (2, 1) and (2, 3)
      # Reuse the previous result if N is already 2.
      p_sdc_n_2_m_1 = 0
      p_actual_failure_n_2_m_1 = 0
      if max_reexec_RTailor == 2:
        p_sdc_n_2_m_1 = p_sdc_RTailor
        p_actual_failure_n_2_m_1 = p_sdc_RTailor
      else:
        p_sdc_n_2_m_1 = compute_p_sdc(task, 2, 1)
        p_actual_failure_n_2_m_1 = p_due_re_exec + p_sdc_n_2_m_1
      
      p_sdc_n_2_m_3 = compute_p_sdc(task, 2, 3)
      p_actual_failure_n_2_m_3 = p_due_re_exec + p_sdc_n_2_m_3

      does_n_2_m_1_satisfy = p_actual_failure_n_2_m_1 < fr_exec
      does_n_2_m_3_satisfy = p_actual_failure_n_2_m_3 < fr_exec
      output.append([task.id, task.execution_time, task.period, task.fr_hour, max_reexec_Reghenzani, max_reexec_RTailor, does_RTailor_satisfy, does_n_2_m_1_satisfy, does_n_2_m_3_satisfy, fr_exec, p_due_re_exec, p_sdc_RTailor, p_actual_failure_RTailor, p_sdc_n_2_m_1, p_sdc_n_2_m_3, ])
    else:
      output.append([task.id, task.execution_time, task.period, task.fr_hour, max_reexec_Reghenzani, max_reexec_RTailor, does_RTailor_satisfy, -1, -1, fr_exec, p_due_re_exec, p_sdc_RTailor, p_actual_failure_RTailor, -1, -1])
  df = pd.DataFrame(output, columns=['id', 'ET', 'Period', 'RequiredFailureRate', 'N_Reghenzani', 'N_RTailor', 'does_RTailor_satisfy', 'does_n_2_m_1_satisfy', 'does_n_2_m_3_satisfy', 'ScaledFailureRate', 'p_due_RTailor', 'p_sdc_RTailor', 'p_actual_failure_RTailor', 'p_sdc_n_2_m_1', 'p_sdc_n_2_m_3'])
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
    main_loop(5, 0.1, 0.33)
    exit()

  # Make tuples of (n, NU, Lambda)
  for n in [5, 10, 25, 50]:
    for lb in [1e-2, 1e-3, 1e-4, 1e-5]:
      u = 0.33
      main_loop(n, lb, u)
      # for u in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
      # for u in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        
if __name__ == "__main__":
  main()