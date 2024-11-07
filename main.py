import os
import argparse
import pandas as pd

t = 0 # Total Execution Time
task_set = [] # Input task set
def readCSV():
    global task_set
    file_name = 'input.csv'
    if not os.path.isfile(file_name):
        print(f"No file named {file_name}.")
        return
    
    try:
        df = pd.read_csv('input.csv')
        task_set = df.values.tolist()
    except Exception as e:
        print("File reading failed with error {e}")

# def edf_schedulability_test():
#     current_time = 0
#     while current_time < t:
#         current_time += 1

def main():
    global t
    global task_set
    parser = argparse.ArgumentParser(description="Schedulability test with EDF scheduler")
    parser.add_argument('-t', '--total', type=int, nargs=1, help="Total Execution time")
    
    # Parse arguments
    args = parser.parse_args()
    t = args.total[0]

    print(f"Total Execution Time: {t}")

    readCSV()
    # Print the stored data to verify
    for entry in task_set:
        print(entry)

if __name__ == "__main__":
    main()