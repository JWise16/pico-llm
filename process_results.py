import json
import os
import csv
from pathlib import Path
from collections import defaultdict

# Define the prompts
PROMPTS = [
    "basic",
    "wall_following",
    "systematic",
    "english",
    "spiral",
    "snake",
    "zigzag"
]

def process_results_folder(folder_path):
    results = defaultdict(lambda: defaultdict(list))
    
    # Get all model folders
    model_folders = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d)) and d.startswith('claude')]
    
    for model in model_folders:
        model_path = os.path.join(folder_path, model)
        
        # Get all run folders
        run_folders = [d for d in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, d)) and d.startswith('run_')]
        
        for run_folder in sorted(run_folders):
            run_path = os.path.join(model_path, run_folder)
            
            for prompt in PROMPTS:
                result_file = os.path.join(run_path, f"{prompt}_results.json")
                if os.path.exists(result_file):
                    with open(result_file, 'r') as f:
                        data = json.load(f)
                        results[model][prompt].append({
                            'coverage': data['coverage'],
                            'success': data['success']
                        })
    
    return results

def create_csv_files(results):
    for model, prompt_data in results.items():
        csv_filename = f"{model}.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            header = ['Prompt'] + [f'Run {i+1}' for i in range(10)] + ['Avg. Coverage', 'Success Rate']
            writer.writerow(header)
            
            # Write data for each prompt
            for prompt in PROMPTS:
                if prompt in prompt_data:
                    runs = prompt_data[prompt]
                    row = [prompt]
                    
                    # Add coverage for each run
                    for run in runs:
                        row.append(f"{run['coverage']:.2f}")
                    
                    # Pad with empty values if less than 10 runs
                    while len(row) < 11:
                        row.append("")
                    
                    # Calculate average coverage
                    avg_coverage = sum(r['coverage'] for r in runs) / len(runs)
                    row.append(f"{avg_coverage:.2f}")
                    
                    # Calculate success rate
                    success_rate = sum(1 for r in runs if r['success']) / len(runs) * 100
                    row.append(f"{success_rate:.2f}%")
                    
                    writer.writerow(row)

def main():
    # Process both analysis folders
    results1 = process_results_folder('results/claude_analysis_20250427_215229')
    results2 = process_results_folder('results/claude_analysis_20250427_230601')
    
    # Merge results from both folders
    all_results = defaultdict(lambda: defaultdict(list))
    for model, prompt_data in results1.items():
        for prompt, runs in prompt_data.items():
            all_results[model][prompt].extend(runs)
    
    for model, prompt_data in results2.items():
        for prompt, runs in prompt_data.items():
            all_results[model][prompt].extend(runs)
    
    # Create CSV files
    create_csv_files(all_results)

if __name__ == "__main__":
    main() 