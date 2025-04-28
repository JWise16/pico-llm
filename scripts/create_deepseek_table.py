#!/usr/bin/env python3
"""Script to create CSV table for deepseek-r1-distill-llama-70b model performance analysis."""

import os
import json
from pathlib import Path
import csv
from statistics import mean

def get_coverage_from_json(json_path):
    """Get coverage value from a JSON results file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get('coverage', 0) * 100  # Convert to percentage
    except Exception as e:
        print(f"Error reading {json_path}: {str(e)}")
        return 0

def create_model_table(model_dir, output_path):
    """Create a CSV table for a single model's performance."""
    # Initialize results dictionary
    prompts = ['basic', 'english', 'snake', 'spiral', 'systematic', 'wall_following', 'zigzag']
    results = {prompt: {} for prompt in prompts}
    
    # Process each run
    for run_num in range(1, 11):
        # Find the run directory by matching the pattern
        run_pattern = f"run_{run_num}_*"
        matching_dirs = list(model_dir.glob(run_pattern))
        
        if matching_dirs:
            run_dir = matching_dirs[0]
            
            # Process each prompt
            for prompt in prompts:
                json_file = run_dir / f"{prompt}_results.json"
                if json_file.exists():
                    coverage = get_coverage_from_json(json_file)
                    results[prompt][f'Run {run_num}'] = coverage
                else:
                    print(f"Results file not found: {json_file}")
                    results[prompt][f'Run {run_num}'] = 0
        else:
            print(f"Run directory not found for run {run_num} in {model_dir}")
            for prompt in prompts:
                results[prompt][f'Run {run_num}'] = 0
    
    # Calculate averages and success rates
    for prompt in prompts:
        coverages = [results[prompt].get(f'Run {i}', 0) for i in range(1, 11)]
        non_zero_coverages = [c for c in coverages if c > 0]
        results[prompt]['Avg. Coverage'] = mean(non_zero_coverages) if non_zero_coverages else 0
        results[prompt]['Success Rate'] = sum(1 for c in coverages if c > 0) / len(coverages) * 100
    
    # Write to CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        header = ['Prompt'] + [f'Run {i}' for i in range(1, 11)] + ['Avg. Coverage', 'Success Rate']
        writer.writerow(header)
        
        # Write data
        for prompt in prompts:
            row = [prompt]
            for run_num in range(1, 11):
                row.append(f"{results[prompt].get(f'Run {run_num}', 0):.2f}%")
            row.append(f"{results[prompt]['Avg. Coverage']:.2f}%")
            row.append(f"{results[prompt]['Success Rate']:.1f}%")
            writer.writerow(row)

def main():
    base_dir = Path('results/groq_analysis_20250428_033801')
    model = 'deepseek-r1-distill-llama-70b'
    model_dir = base_dir / model
    
    if model_dir.exists():
        output_path = base_dir / f'{model}_performance.csv'
        print(f"\nProcessing {model}...")
        create_model_table(model_dir, output_path)
        print(f"Created performance table for {model}")
    else:
        print(f"Model directory not found: {model_dir}")

if __name__ == '__main__':
    main() 