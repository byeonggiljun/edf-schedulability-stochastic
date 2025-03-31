import argparse
from dataclasses import dataclass
from enum import IntEnum
import logging
import math
import random
import os
import sys
import pandas
import pathlib
from collections import defaultdict

# Create result storage
results = {
    'reghenzani_better': defaultdict(list),
    'rtailor_better': defaultdict(list),
    'new_reghenzani_improved': defaultdict(list),  # New case: new_feasible_Reghenzani=True, feasible_Reghenzani=False
    'new_rtailor_improved': defaultdict(list)      # New case: new_feasible_RTailor=True, feasible_RTailor=False
}

# Get the current directory
current_dir = str(pathlib.Path().resolve())

# Recursively find all HOURx directories
def process_all_folders():
    # Find all n* directories
    n_dirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d)) and d.startswith('n')]
    
    for n_dir in n_dirs:
        n_path = os.path.join(current_dir, n_dir)
        
        # Find all u* directories within each n directory
        u_dirs = [d for d in os.listdir(n_path) if os.path.isdir(os.path.join(n_path, d)) and d.startswith('u')]
        
        for u_dir in u_dirs:
            u_path = os.path.join(n_path, u_dir)
            
            # Find all HOUR* directories within each u directory
            hour_dirs = [d for d in os.listdir(u_path) if os.path.isdir(os.path.join(u_path, d)) and d.startswith('HOUR')]
            
            for hour_dir in hour_dirs:
                folder_path = os.path.join(u_path, hour_dir)
                process_folder(folder_path, f"{n_dir}/{u_dir}/{hour_dir}")

# Process a single HOUR folder
def process_folder(folder_path, folder_identifier):
    reghenzani_better_count = 0
    rtailor_better_count = 0
    new_reghenzani_improved_count = 0
    new_rtailor_improved_count = 0
    
    print(f"Processing {folder_identifier}...")
    
    # Process all CSV files in the folder
    for i in range(1, 1000):
        filepath = os.path.join(folder_path, f"TaskSet{i}.csv")
        
        # Skip if file doesn't exist
        if not os.path.exists(filepath):
            continue
            
        try:
            csvFile = pandas.read_csv(filepath)
            
            # Check if all the required columns exist
            required_columns = ["feasible_Reghenzani", "feasible_RTailor", 
                               "new_feasible_Reghenzani", "new_feasible_RTailor"]
            
            if all(col in csvFile.columns for col in required_columns):
                # Extract values
                feasible_Reghenzani = csvFile["feasible_Reghenzani"][0]
                feasible_RTailor = csvFile["feasible_RTailor"][0]
                new_feasible_Reghenzani = csvFile["new_feasible_Reghenzani"][0]
                new_feasible_RTailor = csvFile["new_feasible_RTailor"][0]
                
                # Convert to proper boolean if needed
                if isinstance(feasible_Reghenzani, str):
                    feasible_Reghenzani = feasible_Reghenzani.lower() == 'true'
                if isinstance(feasible_RTailor, str):
                    feasible_RTailor = feasible_RTailor.lower() == 'true'
                if isinstance(new_feasible_Reghenzani, str):
                    new_feasible_Reghenzani = new_feasible_Reghenzani.lower() == 'true'
                if isinstance(new_feasible_RTailor, str):
                    new_feasible_RTailor = new_feasible_RTailor.lower() == 'true'
                
                # Case 1: Reghenzani is better than RTailor
                if feasible_Reghenzani and not feasible_RTailor:
                    results['reghenzani_better'][folder_identifier].append(filepath)
                    reghenzani_better_count += 1
                
                # Case 2: RTailor is better than Reghenzani
                if feasible_RTailor and not feasible_Reghenzani:
                    results['rtailor_better'][folder_identifier].append(filepath)
                    rtailor_better_count += 1
                
                # Case 3: New Reghenzani improves over original Reghenzani
                if new_feasible_Reghenzani and not feasible_Reghenzani:
                    results['new_reghenzani_improved'][folder_identifier].append(filepath)
                    new_reghenzani_improved_count += 1
                
                # Case 4: New RTailor improves over original RTailor
                if new_feasible_RTailor and not feasible_RTailor:
                    results['new_rtailor_improved'][folder_identifier].append(filepath)
                    new_rtailor_improved_count += 1
                    
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
    
    print(f"  Found {reghenzani_better_count} cases where Reghenzani is better")
    print(f"  Found {rtailor_better_count} cases where RTailor is better")
    print(f"  Found {new_reghenzani_improved_count} cases where new Reghenzani improves over original")
    print(f"  Found {new_rtailor_improved_count} cases where new RTailor improves over original")

# Main function
def main():
    process_all_folders()
    
    # Print summary
    print("\n\n===== SUMMARY =====")
    
    print("\nReghenzani better cases:")
    reghenzani_total = 0
    for folder, filepaths in results['reghenzani_better'].items():
        print(f"\n{folder} ({len(filepaths)} cases):")
        for filepath in filepaths:
            print(f"  {filepath}")
        reghenzani_total += len(filepaths)
    
    print(f"\nTotal Reghenzani better cases: {reghenzani_total}")
    
    print("\nRTailor better cases:")
    rtailor_total = 0
    for folder, filepaths in results['rtailor_better'].items():
        print(f"\n{folder} ({len(filepaths)} cases):")
        for filepath in filepaths:
            print(f"  {filepath}")
        rtailor_total += len(filepaths)
    
    print(f"\nTotal RTailor better cases: {rtailor_total}")
    
    print("\nNew Reghenzani improvement cases:")
    new_reghenzani_total = 0
    for folder, filepaths in results['new_reghenzani_improved'].items():
        print(f"\n{folder} ({len(filepaths)} cases):")
        for filepath in filepaths:
            print(f"  {filepath}")
        new_reghenzani_total += len(filepaths)
    
    print(f"\nTotal new Reghenzani improvement cases: {new_reghenzani_total}")
    
    print("\nNew RTailor improvement cases:")
    new_rtailor_total = 0
    for folder, filepaths in results['new_rtailor_improved'].items():
        print(f"\n{folder} ({len(filepaths)} cases):")
        for filepath in filepaths:
            print(f"  {filepath}")
        new_rtailor_total += len(filepaths)
    
    print(f"\nTotal new RTailor improvement cases: {new_rtailor_total}")

if __name__ == "__main__":
    main()