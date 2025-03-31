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
  max_reexec_Reghenzani: int
  new_max_reexec_Reghenzani: int
  max_reexec_RTailor: int
  new_max_reexec_RTailor: int
  max_reexec_PREFACE: int
  max_proact_PREFACE: int

time_unit = 1e-4 # Time unit is 1 ms.
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

def compute_p_fault_RTailor(task, lb, max):
  p_due_sdc_unit = 1 - ((1 - lb * (task.due_portion + task.sdc_portion)) ** (1 / k)) # Eq 2
  # print(f"lb = {lb}, due_portion = {task.due_portion}, k = {k}, p_due_unit = {p_due_unit}")

  p_due_sdc_exec = 1 - (1 - p_due_sdc_unit) ** (task.execution_time) # Eq 3
  # print(f"p_due_unit = {p_due_unit}, exec time = {task.execution_time}, p_due_exec = {p_due_exec}")
  p_due_sdc_reexec = p_due_sdc_exec ** (1 + max) # Eq 5
  # print(f"p_due_reexec = {p_due_reexec}, p_due_exec = {p_due_exec}")

  return p_due_sdc_reexec

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

def compute_avg_utilization(task, lb, max_reexec, max_proact):
  # print(f"***********compute_p_sdc with max_reexec {max_reexec}, max_proact {max_proact}*************")
  p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
  # print(f"p_due_unit = {p_due_unit}, p_sdc_unit = {p_sdc_unit}, p_benign_unit = {p_benign_unit}")
  
  p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9
  # print(f"p_due_exec = {p_due_exec}, p_sdc_exec = {p_sdc_exec}, p_benign_exec = {p_benign_exec}")

  avg_utilization = 0
  verify = 0
  for m in range(0, max_proact + 1): # from 1 to max_proact
    # print(f"*********m = {m}**********")
    p_completed_m = 0
    if m < max_proact:
      # print(f"m = {m} < max_proact = {max_proact}")
      p_completed_m = math.comb((1 + max_reexec), m) * (p_due_exec ** (max_reexec + 1 - m)) * ((1 - p_due_exec) ** m) #Eq 14-1
      avg_utilization += task.execution_time * (1 + max_reexec) * p_completed_m / task.period
    elif m == max_proact:
      # print(f"m = {m} = max_proact = {max_proact}")
      for n in range(m, 2 + max_reexec): # from M to 1 + N
        # print(f"n = {n}, math.comb({n - 1}, {m - 1}) = {math.comb(n - 1, m - 1)}, p_due_exec^{n - m}, (1 - p_due_exec)^{m}")
        prob = math.comb(n - 1, m - 1) * (p_due_exec ** (n - m)) * ((1 - p_due_exec) ** m) # Eq 14-2
        avg_utilization += task.execution_time * n * prob / task.period
        p_completed_m += math.comb(n - 1, m - 1) * (p_due_exec ** (n - m)) * ((1 - p_due_exec) ** m) # Eq 14-2

    # Execution time
    # print(f"avg = {avg_utilization} ET = {task.execution_time}, m = {m}, p_completed_m = {p_completed_m}, period = {task.period}")

    verify += p_completed_m
  # if verify != 1 :
  #   print("Not 1")
  # else:
  #   print("Is 1")
  return avg_utilization

###############################
def generate_task_set(n, lb, u, base_directory, task_set_id):
  tasks = []
  output = []

  zero_detected = False
  while True:
    utilizations = uunifast(n, u)
    for i in range(0, n):
      # Assign a random period.
      period = random.randint(500, 10000)

      fr_index = random.randint(0, len(required_failure_rates) -1)
      # fr_index = 3
      due_portion, sdc_portion = due_sdc_rates[random.randint(0, len(due_sdc_rates) - 1)]
      execution_time = math.floor(utilizations[i] * period)
      if execution_time == 0:
        zero_detected = True
        break
      new_task = Task(id=i, execution_time=execution_time, period=period, due_portion=due_portion, sdc_portion=sdc_portion,
                      fr_index=fr_index, max_reexec_Reghenzani=-1, new_max_reexec_Reghenzani=-1, max_reexec_RTailor=-1,
                       new_max_reexec_RTailor = -1, max_reexec_PREFACE=-1, max_proact_PREFACE=-1)
      tasks.append(new_task)
    if zero_detected:
      tasks = []
      zero_detected = False
    else:
      break


  total_utilization_Reghenzani = 0
  meet_fr_Reghenzani = True
  new_Reghenzani_possible = True
  new_total_utilization_Reghenzani = 0
  avg_utilization_new_Reghenzani = 0

  total_utilization_RTailor = 0
  meet_fr_RTailor = True
  new_RTailor_possible = True
  new_total_utilization_RTailor = 0
  avg_utilization_new_RTailor = 0

  total_utilization_PREFACE = 0
  avg_utilization_PREFACE = 0
  for task in tasks:
    required_fr = required_failure_rates[task.fr_index]
    fr_exec = 1 - ((1 - required_fr) ** (task.period / k))
    N_Reghenzani_found = False
    N_RTailor_found = False
    N_PREFACE_found = False
    for max_reexec_cand in range(0, 10):
      required_fr = required_failure_rates[task.fr_index] # Allocate a required failure rate.
      p_due_reexec = compute_p_due_reexec(task, lb, max_reexec_cand)
      p_sdc_m_1 = compute_p_sdc(task, lb, max_reexec_cand, 1)

      if not N_Reghenzani_found:
        p_fault_Reghenzani = compute_p_fault_Reghenzani(task, lb, max_reexec_cand)
        if p_fault_Reghenzani < fr_exec:
          N_Reghenzani_found = True
          task.max_reexec_Reghenzani = max_reexec_cand
          task.new_max_reexec_Reghenzani = max_reexec_cand
          total_utilization_Reghenzani += task.execution_time * (1 + task.max_reexec_Reghenzani) / task.period

          if p_due_reexec + p_sdc_m_1 > fr_exec:
            meet_fr_Reghenzani = False
            if p_sdc_m_1 > fr_exec:
              new_Reghenzani_possible = False
            if new_Reghenzani_possible and p_sdc_m_1 < fr_exec:
              # There's a chance to meet the requirement by increasing N.
              # Also, until now, there was no task that is impossible to meet the requirement using only N.
              new_max_reexec_Reghenzani = max_reexec_cand
              while True:
                if new_max_reexec_Reghenzani > 10:
                  sys.exit("n larger than 10")
                new_p_due_reexec = compute_p_due_reexec(task, lb, new_max_reexec_Reghenzani)
                if new_p_due_reexec + p_sdc_m_1 < fr_exec:
                  task.new_max_reexec_Reghenzani = new_max_reexec_Reghenzani
                  break
                new_max_reexec_Reghenzani += 1
          new_total_utilization_Reghenzani += task.execution_time * (1 + task.new_max_reexec_Reghenzani) / task.period
          avg_utilization_new_Reghenzani += compute_avg_utilization(task, lb, task.new_max_reexec_Reghenzani, 1)

      if not N_RTailor_found:
        p_fault_RTailor = compute_p_fault_RTailor(task, lb, max_reexec_cand)
        if p_fault_RTailor < fr_exec:
          N_RTailor_found = True
          task.max_reexec_RTailor = max_reexec_cand
          task.new_max_reexec_RTailor = max_reexec_cand
          total_utilization_RTailor += task.execution_time * (1 + task.max_reexec_RTailor) / task.period

          if p_due_reexec + p_sdc_m_1 >= fr_exec:
            meet_fr_RTailor= False
            if p_sdc_m_1 > fr_exec:
              new_RTailor_possible = False
            if new_RTailor_possible and p_sdc_m_1 < fr_exec:
              # There's a chance to meet the requirement by increasing N.
              # Also, until now, there was no task that is impossible to meet the requirement using only N.
              new_max_reexec_RTailor = max_reexec_cand
              while True:
                if new_max_reexec_RTailor > 10:
                  sys.exit("n larger than 10")
                new_p_due_reexec = compute_p_due_reexec(task, lb, new_max_reexec_RTailor)
                if new_p_due_reexec + p_sdc_m_1 < fr_exec:
                  task.new_max_reexec_RTailor = new_max_reexec_RTailor
                  break
                new_max_reexec_RTailor += 1
          new_total_utilization_RTailor += task.execution_time * (1 + task.new_max_reexec_RTailor) / task.period
          avg_utilization_new_RTailor += compute_avg_utilization(task, lb, task.new_max_reexec_RTailor, 1)

      if not N_PREFACE_found:
        max_proact_PREFACE = find_max_proactive(task, lb, max_reexec_cand, p_due_reexec)
        if max_proact_PREFACE != -1:
          N_PREFACE_found = True
          task.max_reexec_PREFACE = max_reexec_cand
          task.max_proact_PREFACE = max_proact_PREFACE
          total_utilization_PREFACE += task.execution_time * (1 + task.max_reexec_PREFACE) / task.period

          avg_utilization_PREFACE += compute_avg_utilization(task, lb, task.max_reexec_PREFACE, task.max_proact_PREFACE)

      if N_Reghenzani_found and N_RTailor_found and N_PREFACE_found:
        break

    output.append([task.id, task.execution_time, task.period, task.due_portion, task.sdc_portion,
                   required_failure_rates_hours[task.fr_index], task.max_reexec_Reghenzani, task.new_max_reexec_Reghenzani,
                   task.max_reexec_RTailor, task.new_max_reexec_RTailor, task.max_reexec_PREFACE, task.max_proact_PREFACE])
    
    if (task.max_reexec_Reghenzani == -1 or task.max_reexec_RTailor == -1 or 
    task.max_reexec_PREFACE == -1 or task.max_proact_PREFACE == -1):
      sys.exit(f"N_Regehnzani = {task.max_reexec_Reghenzani}, N_RTailor = {task.max_reexec_RTailor}, N = {task.max_reexec_PREFACE}, M = {max_proact_PREFACE}")
  
  feasible_Reghenzani = meet_fr_Reghenzani and total_utilization_Reghenzani < 1
  new_feasible_Reghenzani = new_Reghenzani_possible and new_total_utilization_Reghenzani < 1
  feasible_RTailor = meet_fr_RTailor and total_utilization_RTailor < 1
  new_feasible_RTailor = new_RTailor_possible and new_total_utilization_RTailor < 1
  feasible_PREFACE = total_utilization_PREFACE < 1
  # result = [feasible_Reghenzani, meet_fr_Reghenzani, feasible_RTailor, meet_fr_RTailor, feasible_PREFACE]
  df_result = pd.DataFrame({'feasible_Reghenzani':[feasible_Reghenzani], 'new_feasible_Reghenzani': [new_feasible_Reghenzani], 'new_util_Reghenzani': [new_total_utilization_Reghenzani], 'avg_util_new_Reghenzani':[avg_utilization_new_Reghenzani],\
                            'feasible_RTailor':[feasible_RTailor], 'new_feasible_RTailor':[new_feasible_RTailor], 'new_util_RTailor':[new_total_utilization_RTailor], 'avg_util_new_RTailor':[avg_utilization_new_RTailor],\
                            'util_PREFACE':[total_utilization_PREFACE], 'avg_util_PREFACE':[avg_utilization_PREFACE]})
  df_tasks = pd.DataFrame(output, columns=['id', 'ET', 'Period', 'DUE', 'SDC', 'Lambda', 'N_Reghenzani', 'N_new_Reghenzani', 'N_RTailor', 'new_N_RTailor', 'N', 'M'])
  df = pd.concat([df_result, df_tasks], ignore_index=True)
  
  output_path = os.path.join(base_directory, f"TaskSet{task_set_id}.csv")
  df.to_csv(output_path, index=False)
  return feasible_Reghenzani, new_feasible_Reghenzani, feasible_RTailor, new_feasible_RTailor,\
      feasible_PREFACE, avg_utilization_new_Reghenzani, avg_utilization_new_RTailor, avg_utilization_PREFACE
  # Now, check the p_sdc.
  # Count
  # 1. Is this task set scheduable by Reghenzani?
  # 2. If this task set is schedulable by Rheghenzani, does failure rate meets the requirement?
  # 3. Is this task set schedulable by RTailor?
  # 4. If this task set is schedulable by RTailor, does failure rate meets the requirement?
  # 5. Is this task set schedulable by PREFACE?
  # 6. For those tasks that fail to meet requirements using RTailor but succeed with PREFACE,
  # how much slack does each mechanism have?

def get_u_num(u):
  if u == 0.8:
    return 8
  if u == 0.7:
    return 7
  elif u == 0.6:
    return 6
  elif u == 0.5:
    return 5
  elif u == 0.4:
    return 4
  elif u == 0.3:
    return 3
  elif u == 0.2:
    return 2
  elif u == 0.1:
    return 1
  sys.exit("This shouldn't be entered.")
  return None

def main_loop(n, lb, lb_unit, u, num_task_sets):
  global k, required_failure_rates
  if (lb_unit != TimeUnit.HOUR):
    required_failure_rates =  [1 - (1 - rate) ** (1/lb_unit) for rate in required_failure_rates_hours] # rate per min
  else:
    required_failure_rates = required_failure_rates_hours
  k = TimeUnit.SEC/(lb_unit * time_unit)

  # find_max_reexec_proact(Task(id=0, execution_time=146, period=3981, due_portion=0.255, sdc_portion=0.019, fr_index=3, max_reexec_PREFACE=-1, max_proact_PREFACE=-1), lb)

  lb_exponent = int(abs(math.log10(lb)))
  # int(str(lb).split('e')[1].replace('-', ''))
  u_num = get_u_num(u)
  base_directory = os.path.join(os.getcwd(), f"n{n}", f"u{u_num}", f"{lb_unit.name}{lb_exponent}")
  os.makedirs(base_directory, exist_ok=True)
  # generate_task_set(n, lb, u, base_directory, 1)

  num_Reghenzani_success = 0
  num_new_Reghenzani_success = 0
  num_RTailor_success = 0
  num_new_RTailor_success = 0
  num_PREFACE_success = 0
  
  mean_avg_util_new_Reghenzani = 0
  mean_avg_util_new_RTailor = 0
  mean_avg_util_PREFACE = 0

  num_all_success = 0
  for i in range(1, num_task_sets + 1):
    feasible_Reghenzani, new_feasible_Reghenzani, feasible_RTailor, new_feasible_RTailor,\
      feasible_PREFACE, avg_utilization_PREFACE, avg_utilization_new_Reghenzani, avg_utilization_new_RTailor,\
        = generate_task_set(n, lb, u, base_directory, i)
    if feasible_Reghenzani:
      num_Reghenzani_success += 1
    if new_feasible_Reghenzani:
      num_new_Reghenzani_success += 1
    if feasible_RTailor:
      num_RTailor_success += 1
    if new_feasible_RTailor:
      num_new_RTailor_success += 1
    if feasible_PREFACE:
      num_PREFACE_success += 1
    if new_feasible_Reghenzani and new_feasible_RTailor and feasible_PREFACE:
      mean_avg_util_new_Reghenzani = ((mean_avg_util_new_Reghenzani * num_all_success) + avg_utilization_new_Reghenzani) / (num_all_success + 1)
      mean_avg_util_new_RTailor = ((mean_avg_util_new_RTailor * num_all_success) + avg_utilization_new_RTailor) / (num_all_success + 1)
      mean_avg_util_PREFACE = ((mean_avg_util_PREFACE * num_all_success) + avg_utilization_PREFACE) / (num_all_success + 1)
      num_all_success += 1

  return lb_unit.name + str(lb_exponent), num_Reghenzani_success, num_new_Reghenzani_success, \
    num_RTailor_success, num_new_RTailor_success, num_PREFACE_success,\
      mean_avg_util_new_Reghenzani, mean_avg_util_new_RTailor, mean_avg_util_PREFACE

def test(n, lb, lb_unit, u):
  global k, required_failure_rates
  if (lb_unit != TimeUnit.HOUR):
    required_failure_rates =  [1 - (1 - rate) ** (1/lb_unit) for rate in required_failure_rates_hours] # rate per min
  else:
    required_failure_rates = required_failure_rates_hours
  k = TimeUnit.SEC/(lb_unit * time_unit)
  
  for i in range(0, 1):
    generate_task_set(n, lb, u, "", i)

def main():
  global logger
  global p_due_unit, p_benign_unit
  parser = argparse.ArgumentParser(description="Schedulability test with EDF scheduler")
  parser.add_argument('-d', '--debug', action='store_true', help="Debug mode")
  parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")
  parser.add_argument('-t', '--test', action='store_true', help="Test")
  parser.add_argument('-n', '--ntask', nargs=1, type=int, help="Num task sets")

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
    test(1, 1e-5, TimeUnit.HOUR, 0.2)
    exit()
  num_task_sets = args.ntask[0]

  # Make tuples of (n, NU, Lambda)
  for n in [5, 10, 25, 50]:
    df = pd.DataFrame()
    for u in [0.1, 0.2, 0.3, 0.4, 0.5]:
      output = []
      for lb in [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
        name, r1, r2, r3, r4, r5, r6, r7, r8 = main_loop(n, lb, TimeUnit.HOUR, u, num_task_sets)
        output.append([u, name, r1, r2, r3, r4, r5, r6, r7, r8])

      # for lb in [1e-2, 1e-1]:
      #   name, r1, r2, r3, r4 = main_loop(n, lb, TimeUnit.MIN, u, num_task_sets)
      #   output.append([u, name, r1, r2, r3, r4, num_task_sets])
      # for lb in [1e-2]:
      #   name, r1, r2, r3, r4 = main_loop(n, lb, TimeUnit.SEC, u, num_task_sets)
      #   output.append([u, name, r1, r2, r3, r4, num_task_sets])
      util_number = get_u_num(u)
      dff = pd.DataFrame(output, columns=['Utilization', 'Lambda', 'Reghenzani_success', 'new_Reghenzani_success',\
                                          'RTailor_success', 'new_RTailor_success', 'PREFACE_success',\
                                            'avg_util_new_Reghenzani', 'avg_util_new_RTailor', 'avg_util_PREFACE'])
      df = pd.concat([df, dff], axis=1)
      output_path = os.path.join(os.getcwd(), f"n{n}", f"u{util_number}", f"n{n}_u{util_number}_total.csv")
      df.to_csv(output_path, index=False)
    output_path = os.path.join(os.getcwd(), f"n{n}", f"n{n}_total.csv")
    df.to_csv(output_path, index=False)
        
if __name__ == "__main__":
  main()
