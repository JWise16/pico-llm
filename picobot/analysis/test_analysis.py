#!/usr/bin/env python3
"""Test script for the Picobot analysis system."""

import os
import argparse
from pathlib import Path
import time

from picobot.analysis import (
    ExperimentConfig,
    BatchConfig,
    ExperimentRunner,
    ResultsManager
)

def main():
    """Main entry point for testing the analysis system."""
    parser = argparse.ArgumentParser(description="Test the Picobot analysis system")
    parser.add_argument("--output-dir", type=str, default="results/test_analysis",
                      help="Directory to save results (default: results/test_analysis)")
    parser.add_argument("--quick", action="store_true",
                      help="Run a quick test with minimal steps and trials")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a results manager
    results_manager = ResultsManager(str(output_dir))
    
    # Create an experiment runner
    runner = ExperimentRunner(results_manager)
    
    # Set parameters based on quick mode
    steps = 50 if args.quick else 200
    trials = 2 if args.quick else 5
    
    print("\n===== TESTING PICOBOT ANALYSIS SYSTEM =====\n")
    print(f"Output directory: {output_dir}")
    print(f"Steps per trial: {steps}")
    print(f"Number of trials: {trials}")
    print()
    
    # Test 1: Run a single experiment with GPT-3.5-Turbo
    print("Test 1: Running a single experiment with GPT-3.5-Turbo")
    config1 = ExperimentConfig(
        provider="openai",
        model="gpt-3.5-turbo",
        prompt="basic",
        steps=steps,
        trials=trials,
        description="Test experiment with GPT-3.5-Turbo"
    )
    
    start_time = time.time()
    summary1 = runner.run_experiment(config1)
    elapsed = time.time() - start_time
    
    print(f"Experiment completed in {elapsed:.2f} seconds")
    print(f"Average Coverage: {summary1.avg_coverage:.2%}")
    print(f"Average Efficiency: {summary1.avg_efficiency:.2f}")
    print(f"Total Cost: ${summary1.total_cost:.4f}")
    print()
    
    # Test 2: Run a batch of experiments
    print("Test 2: Running a batch of experiments")
    batch = BatchConfig(output_dir=str(output_dir / "batch_test"))
    
    # Add experiments with different prompts
    prompts = ["basic", "wall_following", "systematic"]
    for prompt in prompts:
        config = ExperimentConfig(
            provider="openai",
            model="gpt-3.5-turbo",
            prompt=prompt,
            steps=steps,
            trials=trials,
            description=f"Test experiment with {prompt} prompt"
        )
        batch.add_experiment(config)
    
    start_time = time.time()
    results = runner.run_batch(batch)
    elapsed = time.time() - start_time
    
    print(f"Batch completed in {elapsed:.2f} seconds")
    print(f"Number of experiments: {len(results)}")
    
    for exp_id, summary in results.items():
        print(f"  {summary.config.get('description', exp_id)}:")
        print(f"    Coverage: {summary.avg_coverage:.2%}")
        print(f"    Efficiency: {summary.avg_efficiency:.2f}")
        print(f"    Cost: ${summary.total_cost:.4f}")
    
    print("\nAll tests completed successfully!")
    print(f"Results saved to {output_dir}")

if __name__ == "__main__":
    main() 