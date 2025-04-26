#!/usr/bin/env python3
"""Script to analyze and visualize results from Picobot experiments."""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate

from picobot.analysis import ResultsManager, ExperimentSummary

def load_experiment_results(results_dir: str, experiment_id: Optional[str] = None) -> Dict[str, ExperimentSummary]:
    """Load experiment results from disk.
    
    Args:
        results_dir: Directory containing experiment results
        experiment_id: Optional specific experiment ID to load
        
    Returns:
        Dictionary mapping experiment IDs to their summaries
    """
    results_manager = ResultsManager(results_dir)
    
    if experiment_id:
        summary = results_manager.load_results(experiment_id)
        if summary:
            return {experiment_id: summary}
        return {}
    
    # Load all experiments
    results = {}
    for exp_id in results_manager.list_experiments():
        summary = results_manager.load_results(exp_id)
        if summary:
            results[exp_id] = summary
    
    return results

def create_comparison_table(results: Dict[str, ExperimentSummary]) -> pd.DataFrame:
    """Create a comparison table from experiment results.
    
    Args:
        results: Dictionary of experiment results
        
    Returns:
        DataFrame with comparison data
    """
    data = []
    
    for exp_id, summary in results.items():
        config = summary.config
        
        # Extract experiment details
        description = config.get("description", exp_id)
        provider = config.get("provider", "unknown")
        model = config.get("model", "unknown")
        prompt = config.get("prompt", "unknown")
        use_evolution = config.get("use_evolution", False)
        
        # Create row
        row = {
            "Experiment": description,
            "Provider": provider,
            "Model": model,
            "Prompt": prompt,
            "Evolution": "Yes" if use_evolution else "No",
            "Coverage": summary.avg_coverage,
            "Efficiency": summary.avg_efficiency,
            "Steps": summary.avg_steps,
            "Cells Visited": summary.avg_cells_visited,
            "Cost": summary.total_cost if summary.total_cost is not None else 0.0,
            "Tokens": summary.total_tokens if summary.total_tokens is not None else 0
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

def plot_coverage_comparison(df: pd.DataFrame, output_file: Optional[str] = None) -> None:
    """Plot coverage comparison between experiments.
    
    Args:
        df: DataFrame with experiment results
        output_file: Optional file to save the plot to
    """
    plt.figure(figsize=(12, 6))
    
    # Create grouped bar chart
    x = np.arange(len(df))
    width = 0.35
    
    plt.bar(x, df["Coverage"], width, label="Coverage")
    
    plt.xlabel("Experiment")
    plt.ylabel("Coverage")
    plt.title("Coverage Comparison")
    plt.xticks(x, df["Experiment"], rotation=45, ha="right")
    plt.ylim(0, 1.0)
    plt.legend()
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def plot_efficiency_comparison(df: pd.DataFrame, output_file: Optional[str] = None) -> None:
    """Plot efficiency comparison between experiments.
    
    Args:
        df: DataFrame with experiment results
        output_file: Optional file to save the plot to
    """
    plt.figure(figsize=(12, 6))
    
    # Create grouped bar chart
    x = np.arange(len(df))
    width = 0.35
    
    plt.bar(x, df["Efficiency"], width, label="Efficiency")
    
    plt.xlabel("Experiment")
    plt.ylabel("Efficiency")
    plt.title("Efficiency Comparison")
    plt.xticks(x, df["Experiment"], rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def plot_cost_vs_coverage(df: pd.DataFrame, output_file: Optional[str] = None) -> None:
    """Plot cost vs. coverage scatter plot.
    
    Args:
        df: DataFrame with experiment results
        output_file: Optional file to save the plot to
    """
    # Filter out experiments with no cost data
    cost_df = df[df["Cost"] > 0].copy()
    
    if cost_df.empty:
        print("No cost data available for plotting.")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Create scatter plot
    plt.scatter(cost_df["Cost"], cost_df["Coverage"], s=100)
    
    # Add labels for each point
    for i, row in cost_df.iterrows():
        plt.annotate(
            row["Experiment"],
            (row["Cost"], row["Coverage"]),
            xytext=(5, 5),
            textcoords="offset points"
        )
    
    plt.xlabel("Cost ($)")
    plt.ylabel("Coverage")
    plt.title("Cost vs. Coverage")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def main():
    """Main entry point for the analysis script."""
    parser = argparse.ArgumentParser(description="Analyze Picobot experiment results")
    parser.add_argument("--results-dir", type=str, default="results",
                      help="Directory containing experiment results")
    parser.add_argument("--experiment-id", type=str, default=None,
                      help="Specific experiment ID to analyze")
    parser.add_argument("--output-dir", type=str, default="analysis_output",
                      help="Directory to save analysis output")
    parser.add_argument("--table", action="store_true",
                      help="Print comparison table")
    parser.add_argument("--plot", action="store_true",
                      help="Generate plots")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load results
    results = load_experiment_results(args.results_dir, args.experiment_id)
    
    if not results:
        print(f"No results found in {args.results_dir}")
        return
    
    # Create comparison table
    df = create_comparison_table(results)
    
    # Print table
    if args.table:
        print("\n===== EXPERIMENT COMPARISON =====\n")
        print(tabulate(df, headers="keys", tablefmt="pretty", floatfmt=".3f"))
    
    # Generate plots
    if args.plot:
        print("\nGenerating plots...")
        
        # Coverage comparison
        plot_coverage_comparison(
            df, 
            output_file=str(output_dir / "coverage_comparison.png")
        )
        
        # Efficiency comparison
        plot_efficiency_comparison(
            df, 
            output_file=str(output_dir / "efficiency_comparison.png")
        )
        
        # Cost vs. coverage
        plot_cost_vs_coverage(
            df, 
            output_file=str(output_dir / "cost_vs_coverage.png")
        )
        
        print(f"Plots saved to {output_dir}")
    
    # Save table to CSV
    df.to_csv(output_dir / "comparison.csv", index=False)
    print(f"\nComparison table saved to {output_dir / 'comparison.csv'}")

if __name__ == "__main__":
    main() 