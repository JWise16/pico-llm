#!/usr/bin/env python3
"""Sample script demonstrating how to use the Picobot analysis system."""

import os
import argparse
from typing import List, Dict, Any
import json
from pathlib import Path

from picobot.analysis import (
    ExperimentConfig,
    BatchConfig,
    ExperimentRunner,
    ResultsManager
)

def create_model_comparison_experiments() -> BatchConfig:
    """Create experiments to compare different models."""
    batch = BatchConfig(output_dir="results/model_comparison")
    
    # Models to compare
    models = [
        ("openai", "gpt-3.5-turbo"),
        ("openai", "gpt-4"),
        ("anthropic", "claude-3-sonnet-20240229"),
        ("anthropic", "claude-3-opus-20240229")
    ]
    
    # Create an experiment for each model
    for provider, model in models:
        config = ExperimentConfig(
            provider=provider,
            model=model,
            prompt="basic",
            steps=200,
            trials=3,
            description=f"Testing {model} with basic prompt"
        )
        batch.add_experiment(config)
    
    return batch

def create_prompt_comparison_experiments() -> BatchConfig:
    """Create experiments to compare different prompts."""
    batch = BatchConfig(output_dir="results/prompt_comparison")
    
    # Prompts to compare
    prompts = ["basic", "wall_following", "systematic", "english"]
    
    # Create an experiment for each prompt
    for prompt in prompts:
        config = ExperimentConfig(
            provider="openai",
            model="gpt-3.5-turbo",  # Use a cheaper model for prompt comparison
            prompt=prompt,
            steps=200,
            trials=3,
            description=f"Testing GPT-3.5-Turbo with {prompt} prompt"
        )
        batch.add_experiment(config)
    
    return batch

def create_evolution_comparison_experiments() -> BatchConfig:
    """Create experiments to compare evolution with LLM approaches."""
    batch = BatchConfig(output_dir="results/evolution_comparison")
    
    # Evolution experiment
    evolution_config = ExperimentConfig(
        provider="none",
        model="none",
        use_evolution=True,
        population_size=100,
        generations=50,
        steps=200,
        trials=3,
        description="Testing evolution approach"
    )
    batch.add_experiment(evolution_config)
    
    # LLM experiment for comparison
    llm_config = ExperimentConfig(
        provider="openai",
        model="gpt-3.5-turbo",
        prompt="basic",
        steps=200,
        trials=3,
        description="Testing GPT-3.5-Turbo with basic prompt for comparison"
    )
    batch.add_experiment(llm_config)
    
    return batch

def print_results(results: Dict[str, Any]) -> None:
    """Print experiment results in a readable format."""
    print("\n===== EXPERIMENT RESULTS =====\n")
    
    for exp_id, summary in results.items():
        print(f"Experiment: {summary.config.get('description', exp_id)}")
        print(f"  Average Coverage: {summary.avg_coverage:.2%}")
        print(f"  Average Efficiency: {summary.avg_efficiency:.2f}")
        print(f"  Average Steps: {summary.avg_steps:.1f}")
        print(f"  Average Cells Visited: {summary.avg_cells_visited:.1f}")
        
        if summary.total_cost is not None:
            print(f"  Total Cost: ${summary.total_cost:.4f}")
            print(f"  Total Tokens: {summary.total_tokens}")
        
        print()

def main():
    """Main entry point for the sample experiments script."""
    parser = argparse.ArgumentParser(description="Run Picobot experiments")
    parser.add_argument("--type", choices=["models", "prompts", "evolution", "all"], 
                      default="all", help="Type of experiments to run")
    parser.add_argument("--parallel", action="store_true", 
                      help="Run experiments in parallel")
    parser.add_argument("--workers", type=int, default=None,
                      help="Maximum number of parallel workers")
    args = parser.parse_args()
    
    # Create a results manager
    results_manager = ResultsManager()
    
    # Create an experiment runner
    runner = ExperimentRunner(results_manager)
    
    # Run the selected experiments
    if args.type == "models" or args.type == "all":
        print("\n===== RUNNING MODEL COMPARISON EXPERIMENTS =====\n")
        model_batch = create_model_comparison_experiments()
        model_batch.parallel = args.parallel
        model_batch.max_workers = args.workers
        model_results = runner.run_batch(model_batch)
        print_results(model_results)
    
    if args.type == "prompts" or args.type == "all":
        print("\n===== RUNNING PROMPT COMPARISON EXPERIMENTS =====\n")
        prompt_batch = create_prompt_comparison_experiments()
        prompt_batch.parallel = args.parallel
        prompt_batch.max_workers = args.workers
        prompt_results = runner.run_batch(prompt_batch)
        print_results(prompt_results)
    
    if args.type == "evolution" or args.type == "all":
        print("\n===== RUNNING EVOLUTION COMPARISON EXPERIMENTS =====\n")
        evolution_batch = create_evolution_comparison_experiments()
        evolution_batch.parallel = args.parallel
        evolution_batch.max_workers = args.workers
        evolution_results = runner.run_batch(evolution_batch)
        print_results(evolution_results)
    
    print("\nAll experiments completed!")

if __name__ == "__main__":
    main() 