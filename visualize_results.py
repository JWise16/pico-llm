import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def load_experiment_results(experiment_path):
    """Load experiment results from a summary.json file."""
    with open(experiment_path, 'r') as f:
        return json.load(f)

def create_performance_plots(results, output_dir):
    """Create various performance visualization plots."""
    # Set style
    sns.set_theme(style="whitegrid")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert trials to DataFrame for easier plotting
    trials_df = pd.DataFrame(results['trials'])
    
    # 1. Coverage and Efficiency Plot
    plt.figure(figsize=(10, 6))
    x = range(len(trials_df))
    plt.plot(x, trials_df['coverage'], 'b-o', label='Coverage', linewidth=2, markersize=8)
    plt.plot(x, trials_df['efficiency'], 'r-o', label='Efficiency', linewidth=2, markersize=8)
    plt.xlabel('Trial Number', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('Coverage and Efficiency Across Trials', fontsize=14, pad=20)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'coverage_efficiency.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Steps and Cells Visited Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, trials_df['total_steps'], 'g-o', label='Total Steps', linewidth=2, markersize=8)
    plt.plot(x, trials_df['unique_cells_visited'], 'm-o', label='Cells Visited', linewidth=2, markersize=8)
    plt.xlabel('Trial Number', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title('Steps and Cells Visited Across Trials', fontsize=14, pad=20)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'steps_cells.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Token Usage Plot
    plt.figure(figsize=(10, 6))
    token_data = pd.DataFrame([t['llm_metrics'] for t in results['trials']])
    bars = plt.bar(x, token_data['total_tokens'], color='skyblue', alpha=0.7)
    plt.xlabel('Trial Number', fontsize=12)
    plt.ylabel('Total Tokens', fontsize=12)
    plt.title('Token Usage Across Trials', fontsize=14, pad=20)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=10)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'token_usage.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Cost Analysis Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, token_data['cost'], color='lightgreen', alpha=0.7)
    plt.xlabel('Trial Number', fontsize=12)
    plt.ylabel('Cost ($)', fontsize=12)
    plt.title('API Cost Across Trials', fontsize=14, pad=20)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.4f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cost_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Summary Statistics
    summary_stats = {
        'Average Coverage': f"{results['avg_coverage']:.2%}",
        'Average Efficiency': f"{results['avg_efficiency']:.2f}",
        'Average Steps': f"{results['avg_steps']:.1f}",
        'Average Cells Visited': f"{results['avg_cells_visited']:.1f}",
        'Total Cost': f"${results['total_cost']:.4f}",
        'Total Tokens': f"{results['total_tokens']:,}"
    }
    
    # Create a summary text file
    with open(os.path.join(output_dir, 'summary_stats.txt'), 'w') as f:
        f.write("Experiment Summary Statistics\n")
        f.write("==========================\n\n")
        for key, value in summary_stats.items():
            f.write(f"{key}: {value}\n")

def main():
    # Find all experiment directories
    results_dir = Path('results')
    for experiment_dir in results_dir.glob('**/summary.json'):
        # Create output directory for visualizations
        output_dir = experiment_dir.parent / 'visualizations'
        
        # Load and process results
        results = load_experiment_results(experiment_dir)
        create_performance_plots(results, output_dir)
        print(f"Created visualizations for experiment: {experiment_dir.parent.name}")

if __name__ == '__main__':
    main() 