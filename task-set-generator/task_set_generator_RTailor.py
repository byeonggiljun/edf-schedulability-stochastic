import argparse
from dataclasses import dataclass
from enum import IntEnum
import logging
import math
import random
import os
import pandas as pd
import sys

CUSTOM_LEVEL = 15
logging.addLevelName(CUSTOM_LEVEL, "VERBOSE")

def verbose(self, message, *args, **kwargs):
  if self.isEnabledFor(CUSTOM_LEVEL):
    self._log(CUSTOM_LEVEL, message, args, **kwargs)

logging.Logger.verbose = verbose

logger = logging.getLogger(__name__)
class TimeUnit(IntEnum):
  HOUR = 1
  MIN = 60
  SEC = 3600
  MSEC = 3600000

@dataclass
class Task:
  id: int
  execution_time: int
  period: int
  due_portion: float
  sdc_portion: float
  fr_index: float
  max_reexec_RTailor: int
  max_reexec_Reghenzani: int
  max_reexec_preface: int
  max_proact_preface: int
  new_max_reexec_RTailor: int

time_unit = 1e-4 # Time unit is 100 us.
# time_unit = 0.001 # Time unit is 1 ms.
# time_unit = 1 # Time unit is 1 s.
k = 0

required_failure_rates_hours = [1e-3, 1e-5, 1e-7, 1e-9]
required_failure_rates = []
due_sdc_rates = [[0.264, 0.00019], [0.268, 0.00037], [0.224, 0.00019], [0.279, 0.00019], [0.266, 0.00028], [0.296, 0.00009], [0.255, 0.00019]]

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

def compute_p_fault_Reghenzani(task, lb, max_reexec):
  p_unit = 1 - ((1 - lb) ** (1 / k)) # Eq 4
  p_fault_exec = 1 - (1 - p_unit) ** (task.execution_time) # Eq 1
  p_fault_reexec = p_fault_exec ** (1 + max_reexec) # Eq 3

  return p_fault_reexec

def compute_p_due_reexec(task, lb, max):
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
  # print(f"lb = {lb}, due_portion = {task.due_portion}, k = {k}, p_due_unit = {p_due_unit}")

  p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9d
  # print(f"p_due_unit = {p_due_unit}, exec time = {task.execution_time}, p_due_exec = {p_due_exec}")
  p_due_reexec = p_due_exec ** (1 + max) # Eq 12
  # print(f"p_due_reexec = {p_due_reexec}, p_due_exec = {p_due_exec}")

  return p_due_reexec

def compute_p_sdc(task, lb, max_reexec, max_proact):
  # print(f"***********compute_p_sdc with max_reexec {max_reexec}, max_proact {max_proact}*************")
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
  p_sdc_unit = 1 - ((1 - lb * task.sdc_portion) ** (1 / k)) # Eq 7
  p_benign_unit = 1 - p_due_unit - p_sdc_unit # Eq 8
  # print(f"p_due_unit = {p_due_unit}, p_sdc_unit = {p_sdc_unit}, p_benign_unit = {p_benign_unit}")
  
  p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9
  p_benign_exec = p_benign_unit ** task.execution_time # 11
  p_sdc_exec = 1 - (p_benign_exec + p_due_exec)
  # print(f"p_due_exec = {p_due_exec}, p_sdc_exec = {p_sdc_exec}, p_benign_exec = {p_benign_exec}")

  p_sdc_reexec = 0
  for m in range(1, max_proact + 1): # from 1 to max_proact
    # print(f"*********m = {m}**********")
    p_completed_m = 0
    if m < max_proact:
      # print(f"m = {m} < max_proact = {max_proact}")
      p_completed_m = math.comb((1 + max_reexec), m) * (p_due_exec ** (max_reexec + 1 - m)) * ((1 - p_due_exec) ** m) #Eq 14-1
    elif m == max_proact:
      # print(f"m = {m} = max_proact = {max_proact}")
      for n in range(m, 2 + max_reexec): # from M to 1 + N
        # print(f"n = {n}, math.comb({n - 1}, {m - 1}) = {math.comb(n - 1, m - 1)}, p_due_exec^{n - m}, (1 - p_due_exec)^{m}")
        p_completed_m += math.comb(n - 1, m - 1) * (p_due_exec ** (n - m)) * ((1 - p_due_exec) ** m) # Eq 14-2

    p_sdc_m = 0
    for m_sdc in range(math.ceil(m / 2), m + 1): # From the ceiling of m /2 to m
      # print(f"m_sdc = {m_sdc}")
      p1 = p_sdc_exec / (p_sdc_exec + p_benign_exec)
      p2 = p_benign_exec / (p_sdc_exec + p_benign_exec)
      p_sdc_m += math.comb(m, m_sdc) * (p1 ** m_sdc) * (p2 ** (m - m_sdc)) # Eq 15
    p_sdc_reexec += p_completed_m * p_sdc_m # Eq 13
  return p_sdc_reexec

def find_max_proactive(task, lb, max_reexec, p_due_reexec):
  required_fr = required_failure_rates[task.fr_index]
  max_proact = -1
  for max_proact_cand in range(1, max_reexec + 2, 2): # from 1 to N + 1, only odd numbers.
    p_sdc_reexec = compute_p_sdc(task, lb, max_reexec, max_proact_cand)
    # print(f" m = {max_proact_cand}, p_sdc_reexec = {p_sdc_reexec}")
    fr_exec = 1 - ((1 - required_fr) ** (task.period / k))
    if p_due_reexec + p_sdc_reexec < fr_exec:
      max_proact = max_proact_cand
      break
  return max_proact

def find_max_reexec_proact(task, lb):
  required_fr = required_failure_rates[task.fr_index]
  max_reexec = -1
  max_proact = -1
  for max_reexec_cand in range (0, 10):
    # print(f"------------n = {max_reexec_cand}-----------------------")
    if task.execution_time == 0:
      break

    p_due_reexec = compute_p_due_reexec(task, lb, max_reexec_cand)
    fr_exec = 1 - ((1 - required_fr) ** (task.period / k))
    if p_due_reexec < fr_exec:
      # print(f"******p_due_reexec = {p_due_reexec} < fr_exec = {fr_exec}*******")
      max_proact_cand = find_max_proactive(task, lb, max_reexec_cand, p_due_reexec)
      max_proact = max_proact_cand
      if max_proact_cand == -1:
        continue
      max_reexec = max_reexec_cand
      break
  # print(f"max_reexec = {max_reexec}, max_proact = {max_proact}")

# def find_new_max_reexec(task, lb, p_sdc, fr_exec):
#   logger.debug("--------------------------")
#   logger.debug(f"Fail with n = {task.max_reexec_RTailor}")
#   # Check if the requirement can be met by increasing n
#   p_due = 
#   logger.debug(f"p_due = {p_due_RTailor} p_sdc = {p_sdc}, fr_exec = {fr_exec}")
#   # sys.exit("p_sdc < fr_exec")
#   new_max_reexec_found = False
#   for new_max_reexec_cand in range(task.max_reexec_RTailor, 10):
#     p_due_RTailor = compute_p_due_reexec(task, lb, new_max_reexec_cand)
#     if p_due_RTailor + p_sdc < fr_exec:
#       new_max_reexec_found = True
#       task.new_max_reexec_RTailor = new_max_reexec_cand
#       logger.debug(f"Success with n = {new_max_reexec_cand}")
#       logger.debug(f"N_preface = {task.max_reexec_preface}, M_preface = {task.max_proact_preface}")
#       break
#   if not new_max_reexec_found:
#     sys.exit("new n larger than 9")

def generate_task_set(n, lb, u, base_directory, task_set_id):
  # Distributed utilizations and assign execution time based on RTailor.
  # Compute the slack time
  # Compute P_SDC, record failure rate
  # If failed, modify the max_reexec and max_proact_preface using PREFACE
  # Recompute the total utilization
  # If it's feasible, compute slack time
  # For a tuple (n, lb, u), the rate of failure
  # the rate of failure that PREFACE can fix (how many can we make it work/Total failed sets)
  # Average difference between slack tims of RTailor and PREFACE

  tasks = []
  output = []
  while True:
    utilizations = uunifast(n, u)

    zero_detected = False
    for i in range(0, n):
      # Assign a random period.
      # period = random.randint(500, 10000)
      period = 500

      fr_index = random.randint(0, len(required_failure_rates) -1)
      fr_index = 3
      required_fr = required_failure_rates[fr_index] # Allocate a required failure rate.
      due_portion, sdc_portion = due_sdc_rates[random.randint(0, len(due_sdc_rates) - 1)]
      due_portion, sdc_portion = due_sdc_rates[0]
      new_task = Task(id=i, execution_time=0, period=period, due_portion=due_portion, sdc_portion=sdc_portion, fr_index=fr_index,
                      max_reexec_RTailor=-1, max_reexec_Reghenzani=1, max_reexec_preface=-1, max_proact_preface=-1,
                      new_max_reexec_RTailor = -1)

      for max_reexec_RTailor_cand in range (0, 10):
        # print("-----------------------------------")
        new_task.execution_time = math.floor(utilizations[i] * new_task.period / (1 + max_reexec_RTailor_cand))
        # new_task.execution_time = utilizations[i] * new_task.period # FIXME
        if new_task.execution_time == 0:
          zero_detected = True
          break

        # p_due_reexec = compute_p_due_reexec(new_task, lb, max_reexec_RTailor_cand)
        p_due_reexec = compute_p_fault_Reghenzani(new_task, lb, max_reexec_RTailor_cand) # FIXME
        fr_exec = 1 - ((1 - required_fr) ** (new_task.period / k))
        if p_due_reexec < fr_exec:
          print("-----------------------------------------------------------------")
          print(f"******n = {max_reexec_RTailor_cand}, p_due_reexec = {p_due_reexec} < fr_exec = {fr_exec}*******")
          new_task.max_reexec_RTailor = max_reexec_RTailor_cand
          break
      if zero_detected:
        break

      # We found N by RTailor. Now find N by PREFACE and Reghenzani.
      N_Reghenzani_found = False
      for max_reexec_cand in range (new_task.max_reexec_RTailor, 10):
        # print("-----------------------------------")
        p_due_reexec = compute_p_due_reexec(new_task, lb, max_reexec_cand)
        fr_exec = 1 - ((1 - required_fr) ** (new_task.period / k))
        if p_due_reexec < fr_exec:
          if not N_Reghenzani_found:  
            new_task.max_reexec_Reghenzani = max_reexec_cand
            N_Reghenzani_found = True

          # print(f"******p_due_reexec = {p_due_reexec} < fr_exec = {fr_exec}*******")
          max_proact_cand = find_max_proactive(new_task, lb, max_reexec_cand, p_due_reexec)
          if max_proact_cand == -1:
            continue
          new_task.max_proact_preface = max_proact_cand
          new_task.max_reexec_preface = max_reexec_cand
          break
      if new_task.max_reexec_preface == -1:
        sys.exit("N greater than 9")

      # We found N by Reghenzani and PREFACE.
      tasks.append(new_task)
    if zero_detected:
      logger.debug("Zero detected.")
      tasks = []
    else:
      break
  
  # # We found a vaild task set with N_Reghenzani, N_RTailor, N_PREFACE, and M_PREFACE.
  # # Now, check P_SDC.
  # RTailor_fail = False
  # RTailor_fail_cannot_fix = False
  # utilization_by_RTailor = 0
  # utilization_by_preface = 0
  # for task in tasks:
  #   p_due_RTailor = compute_p_due_reexec(task, lb, task.max_reexec_RTailor)
  #   p_failure_Reghenzani = compute_p_fault_Reghenzani(task, lb, task.max_reexec_Reghenzani)
  #   p_sdc = compute_p_sdc(task, lb, task.max_reexec_RTailor, 1)
  #   required_fr = required_failure_rates[task.fr_index]
  #   fr_exec = 1 - ((1 - required_fr) ** (task.period / k))
  #   if p_due_RTailor + p_sdc >= fr_exec:
  #     RTailor_fail = True
  #     if p_sdc >= fr_exec:
  #       RTailor_fail_cannot_fix = True
  #       logger.verbose("Can't be solve by increasing N")
  #     else:
  #       task.new_max_reexec_RTailor = find_new_max_reexec(task, lb, p_sdc, fr_exec)
  #   # compute the (possibly) new utilization.
  #   utilization_by_RTailor += task.execution_time * (1 + task.new_max_reexec_RTailor) / task.period
  #   utilization_by_preface += task.execution_time * (1 + task.max_reexec_preface) / task.period

  #   output.append([task.id, task.execution_time, task.period, required_failure_rates_hours[task.fr_index],
  #                   task.max_reexec_Reghenzani, task.max_reexec_RTailor, task.new_max_reexec_RTailor,
  #                   task.max_reexec_preface, task.max_proact_preface])

  # print("--------------------------")
  # if utilization_by_RTailor > 1 or RTailor_fail:
  #   print("RTailor fails")
  # if utilization_by_preface > 1:
  #   print("preface fails")
  
  # df = pd.DataFrame(output, columns=['id', 'ET', 'Period', 'RequiredFailureRateHour',
  #                                    'N_Reghenzani', 'N_RTailor', 'N', 'M'])
  # df.to_csv("output_test.csv", index=False)
  
  # return utilization_by_RTailor > 1, RTailor_fail, utilization_by_preface > 1 

def main_loop(n, lb, lb_unit, u, num_task_sets):
  global k, required_failure_rates
  if (lb_unit != TimeUnit.HOUR):
    required_failure_rates =  [1 - (1 - rate) ** (1/lb_unit) for rate in required_failure_rates_hours] # rate per min
  else:
    required_failure_rates = required_failure_rates_hours
  k = TimeUnit.SEC/(lb_unit * time_unit)

  # find_max_reexec_proact(Task(id=0, execution_time=146, period=3981, due_portion=0.255, sdc_portion=0.019, fr_index=3, max_reexec_preface=-1, max_proact_preface=-1), lb)

  lb_str = "{:e}".format(lb)
  lb_exponent = abs(int(lb_str.split('e')[1]))
  base_directory = os.path.join(os.getcwd(), f"n{n}", f"u{int(u/0.1)}", f"{lb_unit.name}{lb_exponent}")
  os.makedirs(base_directory, exist_ok=True)
  # generate_task_set(n, lb, u, base_directory, 1)

  num_success = 0
  num_fail = 0
  for i in range(1, num_task_sets + 1):
    success = generate_task_set(n, lb, u, base_directory, i)
    if success:
      num_success += 1
    else:
      num_fail += 1
  if num_success + num_fail != num_task_sets:
    sys.exit(f"ERROR: num_success {num_success} + num_fail {num_fail} != num_tasks {num_task_sets}")

  return lb_unit.name + str(lb_exponent), num_fail, num_task_sets

def test(n, lb, lb_unit, u):
  global k, required_failure_rates
  if (lb_unit != TimeUnit.HOUR):
    required_failure_rates =  [1 - (1 - rate) ** (1/lb_unit) for rate in required_failure_rates_hours] # rate per min
  else:
    required_failure_rates = required_failure_rates_hours
  k = TimeUnit.SEC/(lb_unit * time_unit)
  
  for i in range(0, 100):
    generate_task_set(n, lb, u, "", i)

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
  if args.test:
    # To test only 1 task, put 1 as the first argument.
    # Number of tasks, fault rate, total utilization.
    # generate_task_set(5, 1e-2, 0.25)
    test(1, 1e-2, TimeUnit.SEC, 0.8)
    exit()

  # Make tuples of (n, NU, Lambda)
  for n in [5, 10, 25, 50]:
    for lb in [1e-2, 1e-3, 1e-4, 1e-5]:
      u = 0.33
      main_loop(n, lb, TimeUnit.HOUR, u, 1)
      # for u in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
      # for u in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        
if __name__ == "__main__":
  main()
