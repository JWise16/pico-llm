#!/usr/bin/env python3
"""Script to create CSV summaries from Groq test results."""

import os
import re
import csv
from pathlib import Path
from datetime import datetime

def parse_summary_file(summary_path):
    """Parse a summary.txt file and return a list of prompt results."""
    results = []
    current_prompt = None
    current_result = {}
    
    with open(summary_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Check for prompt name
            if line.endswith(':'):
                if current_prompt and current_result:
                    results.append((current_prompt, current_result))
                current_prompt = line[:-1]
                current_result = {}
                continue
                
            # Parse metrics
            if line.startswith('  Coverage:'):
                current_result['coverage'] = float(re.search(r'([\d.]+)%', line).group(1))
            elif line.startswith('  Efficiency:'):
                current_result['efficiency'] = float(re.search(r'([\d.]+)', line).group(1))
            elif line.startswith('  Steps:'):
                current_result['steps'] = int(re.search(r'(\d+)', line).group(1))
            elif line.startswith('  Tokens:'):
                current_result['tokens'] = int(re.search(r'(\d+)', line).group(1))
            elif line.startswith('  Cost:'):
                current_result['cost'] = float(re.search(r'\$([\d.]+)', line).group(1))
            elif line.startswith('  Time:'):
                current_result['time'] = float(re.search(r'([\d.]+)s', line).group(1))
            elif line.startswith('  Error:'):
                current_result['error'] = line.split('Error: ')[1]
    
    # Add the last result
    if current_prompt and current_result:
        results.append((current_prompt, current_result))
    
    return results

def create_model_summary(model_dir):
    """Create a CSV summary for a single model."""
    model_name = model_dir.name
    summary_path = model_dir / 'model_summary.csv'
    
    # Collect all results from all runs
    all_results = []
    for run_dir in model_dir.glob('run_*'):
        summary_file = run_dir / 'summary.txt'
        if summary_file.exists():
            try:
                results = parse_summary_file(summary_file)
                all_results.extend(results)
                print(f"Processed {summary_file}")
            except Exception as e:
                print(f"Error processing {summary_file}: {str(e)}")
    
    # Write to CSV
    with open(summary_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['prompt', 'coverage', 'efficiency', 'steps', 'tokens', 'cost', 'time'])
        
        for prompt, result in all_results:
            if 'error' in result:
                writer.writerow([prompt, 'ERROR', result['error'], '', '', '', ''])
            else:
                writer.writerow([
                    prompt,
                    f"{result['coverage']:.2f}%",
                    result['efficiency'],
                    result['steps'],
                    result['tokens'],
                    f"${result['cost']:.4f}",
                    f"{result['time']:.2f}s"
                ])
    
    print(f"Created summary for {model_name}")

def create_overall_summary(base_dir):
    """Create an overall CSV summary for all models."""
    summary_path = base_dir / 'overall_summary.csv'
    
    with open(summary_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['model', 'prompt', 'coverage', 'efficiency', 'steps', 'tokens', 'cost', 'time'])
        
        for model_dir in base_dir.iterdir():
            if not model_dir.is_dir():
                continue
                
            model_name = model_dir.name
            model_summary = model_dir / 'model_summary.csv'
            
            if model_summary.exists():
                with open(model_summary, 'r') as mf:
                    reader = csv.reader(mf)
                    next(reader)  # Skip header
                    for row in reader:
                        writer.writerow([model_name] + row)
    
    print("Created overall summary")

def main():
    # Use the specific directory we want to process
    target_dir = Path('results/groq_analysis_20250428_024145')
    if not target_dir.exists():
        print(f"Directory {target_dir} not found")
        return
    
    print(f"Processing results from {target_dir}")
    
    # Process each Llama 3 model
    llama3_models = [
        'llama-3.3-70b-versatile',
        'llama-3.1-8b-instant',
        'llama-guard-3-8b',
        'llama3-70b-8192',
        'llama3-8b-8192'
    ]
    
    for model in llama3_models:
        model_dir = target_dir / model
        if model_dir.exists():
            create_model_summary(model_dir)
    
    # Create overall summary
    create_overall_summary(target_dir)

if __name__ == '__main__':
    main() 