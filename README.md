# EDF Schedulability Test
## How to use
1. Modfiy 'input.csv' with your task set
2. Run `python3 main.py [-t TIMEOUT] [-d] sample.csv`
3. Check 'output_sample.csv'
4. Test with your own taks sets by modifying sample.csv.

## Policies
1. A task needs to be finished before the next same task comes (deadline = next period). 
2. If deadline violation occurs, execute the task until the deadline and drop it.

## Assumption
1. Every time value is integer (no floating point).
2. The execution time is strictly greater than 0.

## ToDo
- [x] Do not exceed the maximum time.
- [x] Check whether a task has violated the deadline.
    - [x] Drop the task if deadline violation occurs.
- [x] Reschedule if a task has failed.
- [x] Apply N, the maximum allowed number of re-execution;
- [ ] and M, the least required number of successive successful execution.