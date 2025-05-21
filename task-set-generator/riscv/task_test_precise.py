import argparse
from dataclasses import dataclass
from enum import IntEnum
import logging
import sys
import mpmath

# Set high precision for mpmath
mpmath.mp.dps = 100  # Set 100 decimal places of precision

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
    fr_index: int
    max_reexec_Reghenzani: int = -1
    max_reexec_RTailor: int = -1

# Use mpmath for all calculations
time_unit = mpmath.mpf('1e-4')  # Time unit is 0.1 ms.
k = mpmath.mpf('0')

# Convert all constants to mpmath types
required_failure_rates_hours = [mpmath.mpf('1e-3'), mpmath.mpf('1e-5'), 
                              mpmath.mpf('1e-7'), mpmath.mpf('1e-9')]
required_failure_rates = []
due_sdc_rates = [
    [mpmath.mpf('0.0202'), mpmath.mpf('0.0000141')], 
    [mpmath.mpf('0.0227'), mpmath.mpf('0.0000313')], 
    [mpmath.mpf('0.0247'), mpmath.mpf('0.0000204')], 
    [mpmath.mpf('0.0283'), mpmath.mpf('0.0000188')], 
    [mpmath.mpf('0.0174'), mpmath.mpf('0.0000182')], 
    [mpmath.mpf('0.0237'), mpmath.mpf('0.0000074')], 
    [mpmath.mpf('0.0216'), mpmath.mpf('0.0000157')]
]

def format_number(value):
    """Format mpmath values to show small numbers clearly"""
    if value != 0 and abs(value) < mpmath.mpf('1e-10'):
        # Use mpmath's nstr function with explicit e-format and high precision
        return mpmath.nstr(value, n=20, min_fixed=-1, max_fixed=-1)
    # For larger numbers, still use a reasonable precision
    return mpmath.nstr(value, n=15)

def compute_p_fault_Reghenzani(task, lb, max_reexec):
    print("compute_p_fault_Reghenzani")
    # p_unit = 1 - ((1 - lb) ** (1 / k)) # Eq 4
    p_unit = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - lb, mpmath.mpf(1) / k)
    
    # p_fault_exec = 1 - (1 - p_unit) ** (task.execution_time) # Eq 1
    p_fault_exec = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - p_unit, task.execution_time)
    
    print(f"lb = {format_number(lb)}")
    print(f"k = {format_number(k)}")
    print(f"p_unit = {format_number(p_unit)}")
    print(f"p_fault_exec = {format_number(p_fault_exec)}")
    
    # p_fault_reexec = p_fault_exec ** (1 + max_reexec) # Eq 3
    p_fault_reexec = mpmath.power(p_fault_exec, mpmath.mpf(1) + max_reexec)
    
    print(f"p_fault_reexec = {format_number(p_fault_reexec)}")
    return p_fault_reexec

def compute_p_due_reexec(task, lb, max_reexec):
    print("compute_p_due_reexec")
    # p_due_unit = 1 - ((1 - lb * task.due_portion) ** (1 / k)) # Eq 6
    p_due_unit = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - lb * task.due_portion, mpmath.mpf(1) / k)
    
    # p_due_exec = 1 - (1 - p_due_unit) ** (task.execution_time) # Eq 9d
    p_due_exec = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - p_due_unit, task.execution_time)
    
    print(f"lb = {format_number(lb)}")
    print(f"due_portion = {format_number(task.due_portion)}")
    print(f"k = {format_number(k)}")
    print(f"p_due_unit = {format_number(p_due_unit)}")
    print(f"exec time = {task.execution_time}")
    print(f"p_due_exec = {format_number(p_due_exec)}")
    
    # p_due_reexec = p_due_exec ** (1 + max) # Eq 12
    p_due_reexec = mpmath.power(p_due_exec, mpmath.mpf(1) + max_reexec)
    
    print(f"p_due_reexec = {format_number(p_due_reexec)}")
    return p_due_reexec

def compute_p_fault_RTailor(task, lb, max_reexec):
    print("compute_p_fault_RTailor")
    # p_due_sdc_unit = 1 - ((1 - lb * (task.due_portion + task.sdc_portion)) ** (1 / k)) # Eq 2
    p_due_sdc_unit = mpmath.mpf(1) - mpmath.power(
        mpmath.mpf(1) - lb * (task.due_portion + task.sdc_portion), 
        mpmath.mpf(1) / k
    )
    
    # p_due_sdc_exec = 1 - (1 - p_due_sdc_unit) ** (task.execution_time) # Eq 3
    p_due_sdc_exec = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - p_due_sdc_unit, task.execution_time)
    
    print(f"lb = {format_number(lb)}")
    print(f"due_portion = {format_number(task.due_portion)}")
    print(f"sdc_portion = {format_number(task.sdc_portion)}")
    print(f"k = {format_number(k)}")
    print(f"p_due_sdc_unit = {format_number(p_due_sdc_unit)}")
    print(f"p_due_sdc_exec = {format_number(p_due_sdc_exec)}")
    
    # p_due_sdc_reexec = p_due_sdc_exec ** (1 + max) # Eq 5
    p_due_sdc_reexec = mpmath.power(p_due_sdc_exec, mpmath.mpf(1) + max_reexec)
    
    print(f"p_due_sdc_reexec = {format_number(p_due_sdc_reexec)}")
    return p_due_sdc_reexec

def analyze_single_task(lb, lb_unit, execution_time, period, due_sdc_index, fr_index):
    global k, required_failure_rates
    
    # Convert inputs to mpmath
    lb = mpmath.mpf(str(lb))
    execution_time = mpmath.mpf(str(execution_time))
    period = mpmath.mpf(str(period))
    
    # Set up the required failure rates based on time unit
    if (lb_unit != TimeUnit.HOUR):
        required_failure_rates = [
            mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - rate, mpmath.mpf(1)/mpmath.mpf(str(lb_unit))) 
            for rate in required_failure_rates_hours
        ]
    else:
        required_failure_rates = required_failure_rates_hours
    
    # Calculate k constant
    k = mpmath.mpf(TimeUnit.SEC)/(mpmath.mpf(lb_unit) * time_unit)
    
    # Get the due and sdc portions from the list
    due_portion, sdc_portion = due_sdc_rates[due_sdc_index]
    
    # Create task with high precision values
    task = Task(
        id=0, 
        execution_time=int(execution_time),  # Keep as integer
        period=int(period),                 # Keep as integer
        due_portion=due_portion,
        sdc_portion=sdc_portion,
        fr_index=fr_index
    )
    
    required_fr = required_failure_rates[task.fr_index]
    # fr_exec = 1 - ((1 - required_fr) ** (task.period / k))
    fr_exec = mpmath.mpf(1) - mpmath.power(mpmath.mpf(1) - required_fr, task.period / k)
    
    print(f"\n===== Task Analysis Results =====")
    print(f"Execution Time: {task.execution_time}")
    print(f"Period: {task.period}")
    print(f"DUE Portion: {format_number(task.due_portion)}")
    print(f"SDC Portion: {format_number(task.sdc_portion)}")
    print(f"Required Failure Rate: {format_number(required_failure_rates_hours[fr_index])} per hour")
    print(f"k constant: {format_number(k)}")
    print(f"Failure Rate per Execution: {format_number(fr_exec)}")
    
    # Analyze with Reghenzani method
    print("\n1. Reghenzani Method Analysis:")
    for max_reexec_cand in range(0, 10):
        p_fault_Reghenzani = compute_p_fault_Reghenzani(task, lb, max_reexec_cand)
        
        print(f"For max_reexec_cand = {max_reexec_cand}:")
        print(f"p_fault_Reghenzani = {format_number(p_fault_Reghenzani)}")
        print(f"fr_exec = {format_number(fr_exec)}")
        print(f"p_fault_Reghenzani < fr_exec: {p_fault_Reghenzani < fr_exec}")
        
        if p_fault_Reghenzani < fr_exec:
            task.max_reexec_Reghenzani = max_reexec_cand
            utilization = mpmath.mpf(task.execution_time * (1 + task.max_reexec_Reghenzani)) / mpmath.mpf(task.period)
            print(f"  Max Reexecutions: {max_reexec_cand}")
            print(f"  Failure Probability: {format_number(p_fault_Reghenzani)}")
            print(f"  Utilization: {format_number(utilization)}")
            break
    
    if task.max_reexec_Reghenzani == -1:
        print("  No valid max reexecution found for Reghenzani method (up to 10).")
    
    # Analyze with RTailor method
    print("\n2. RTailor Method Analysis:")
    for max_reexec_cand in range(0, 10):
        p_fault_RTailor = compute_p_fault_RTailor(task, lb, max_reexec_cand)
        
        print(f"For max_reexec_cand = {max_reexec_cand}:")
        print(f"p_fault_RTailor = {format_number(p_fault_RTailor)}")
        print(f"fr_exec = {format_number(fr_exec)}")
        print(f"p_fault_RTailor < fr_exec: {p_fault_RTailor < fr_exec}")
        
        if p_fault_RTailor < fr_exec:
            task.max_reexec_RTailor = max_reexec_cand
            utilization = mpmath.mpf(task.execution_time * (1 + task.max_reexec_RTailor)) / mpmath.mpf(task.period)
            print(f"  Max Reexecutions: {max_reexec_cand}")
            print(f"  Failure Probability: {format_number(p_fault_RTailor)}")
            print(f"  Utilization: {format_number(utilization)}")
            break
    
    if task.max_reexec_RTailor == -1:
        print("  No valid max reexecution found for RTailor method (up to 10).")

def main():
    parser = argparse.ArgumentParser(description="Single Task Analysis with High Precision")
    parser.add_argument('-d', '--debug', action='store_true', help="Debug mode")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")
    parser.add_argument('-lb', '--lambda_val', type=float, required=True, help="Error rate (lambda)")
    parser.add_argument('-u', '--timeunit', choices=['hour', 'min', 'sec', 'msec'], 
                       default='hour', help="Time unit for lambda (default: hour)")
    parser.add_argument('-e', '--execution', type=int, required=True, help="Execution time")
    parser.add_argument('-p', '--period', type=int, required=True, help="Period")
    parser.add_argument('-ds', '--duesdc', type=int, default=0, 
                       help="Index for due_sdc_rates array (0-6, default: 0)")
    parser.add_argument('-fr', '--failurerate', type=int, default=2, 
                       help="Index for required failure rates (0-3, default: 2)")

    args = parser.parse_args()

    # Set up logging
    if args.debug:
        print("Debug Mode.")
        logging.basicConfig(level=logging.DEBUG)
    if args.verbose:
        print("Verbose Mode.")
        logging.basicConfig(level=CUSTOM_LEVEL)

    # Set the time unit
    time_unit_map = {
        'hour': TimeUnit.HOUR,
        'min': TimeUnit.MIN,
        'sec': TimeUnit.SEC,
        'msec': TimeUnit.MSEC
    }
    
    # Convert timeunit string to enum
    time_unit_enum = time_unit_map[args.timeunit]
    
    # Validate inputs
    if args.duesdc < 0 or args.duesdc >= len(due_sdc_rates):
        sys.exit(f"Error: duesdc index must be between 0 and {len(due_sdc_rates)-1}")
        
    if args.failurerate < 0 or args.failurerate >= len(required_failure_rates_hours):
        sys.exit(f"Error: failurerate index must be between 0 and {len(required_failure_rates_hours)-1}")
    
    # Run the analysis
    analyze_single_task(
        args.lambda_val,
        time_unit_enum,
        args.execution,
        args.period,
        args.duesdc,
        args.failurerate
    )

if __name__ == "__main__":
    main()