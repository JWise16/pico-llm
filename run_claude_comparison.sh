#!/bin/bash

# Create timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="results/claude_comparison_${TIMESTAMP}"

# Create base directory
mkdir -p "${BASE_DIR}"

# Run test 10 times
for i in {1..10}; do
    echo "Running trial ${i}..."
    OUTPUT_DIR="${BASE_DIR}/trial_${i}"
    mkdir -p "${OUTPUT_DIR}"
    
    # Run test with JUnit XML output going to trial directory
    PICOBOT_OUTPUT_DIR="${OUTPUT_DIR}" \
    python -m pytest tests/scenarios/test_prompt_comparison.py::test_prompt_performance -v \
        --junitxml="${OUTPUT_DIR}/junit.xml"
    
    # Add a small delay between runs to prevent rate limiting
    sleep 5
done

# Create overall summary
echo "Creating overall summary..."
python3 - <<EOF
import json
import os
from pathlib import Path
from datetime import datetime

# Get the base directory from the most recent run
base_dir = sorted(Path("results").glob("claude_comparison_*"))[-1]
print(f"Analyzing results from {base_dir}")

# Initialize results
all_results = {
    'model': None,
    'trials': [],
    'summary': {
        'prompts': {}
    }
}

# Process each trial
for trial_dir in sorted(base_dir.glob("trial_*")):
    trial_data_file = trial_dir / "trial_data.json"
    if not trial_data_file.exists():
        continue
        
    with open(trial_data_file) as f:
        trial_data = json.load(f)
        
    # Set model if not set
    if all_results['model'] is None:
        all_results['model'] = trial_data['model']
        
    # Add trial results
    all_results['trials'].append({
        'timestamp': trial_data['timestamp'],
        'results': trial_data['prompts']
    })
    
    # Update summary statistics
    for prompt, result in trial_data['prompts'].items():
        if prompt not in all_results['summary']['prompts']:
            all_results['summary']['prompts'][prompt] = {
                'coverages': [],
                'steps': [],
                'successes': 0,
                'total_trials': 0
            }
            
        stats = all_results['summary']['prompts'][prompt]
        stats['coverages'].append(result['coverage'])
        stats['steps'].append(result['steps'])
        stats['successes'] += 1 if result['success'] else 0
        stats['total_trials'] += 1

# Calculate averages and success rates
for prompt, stats in all_results['summary']['prompts'].items():
    stats['avg_coverage'] = sum(stats['coverages']) / len(stats['coverages'])
    stats['avg_steps'] = sum(stats['steps']) / len(stats['steps'])
    stats['success_rate'] = (stats['successes'] / stats['total_trials']) * 100

# Save aggregated results
with open(base_dir / "aggregated_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

# Create markdown table
with open(base_dir / "results_table.md", "w") as f:
    f.write(f"# Claude Model Performance Analysis\n\n")
    f.write(f"Model: {all_results['model']}\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Number of Trials: {len(all_results['trials'])}\n\n")
    
    f.write("| Prompt | Avg Coverage | Avg Steps | Success Rate |\n")
    f.write("|--------|--------------|-----------|--------------|\n")
    
    for prompt, stats in sorted(all_results['summary']['prompts'].items()):
        f.write(f"| {prompt.upper()} | {stats['avg_coverage']:.2f}% | {stats['avg_steps']:.1f} | {stats['success_rate']:.1f}% |\n")

print(f"\nAnalysis complete! Results saved in {base_dir}")
print("Check results_table.md for a formatted summary")
EOF

echo "All trials completed. Results are in ${BASE_DIR}" 