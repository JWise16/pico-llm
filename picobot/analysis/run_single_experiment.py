#!/usr/bin/env python3
"""Script to run a single Picobot experiment for testing."""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

from picobot.analysis import ExperimentConfig, ExperimentRunner, ResultsManager

def main():
    """Main entry point for running a single experiment."""
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run a single Picobot experiment")
    
    # Experiment parameters
    parser.add_argument("--provider", choices=["openai", "anthropic", "none"], default="openai",
                      help="LLM provider to use (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                      help="Model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--prompt", type=str, default="basic",
                      help="Prompt to use (default: basic)")
    parser.add_argument("--temperature", type=float, default=0.7,
                      help="Temperature for generation (default: 0.7)")
    parser.add_argument("--steps", type=int, default=200,
                      help="Number of steps to run (default: 200)")
    parser.add_argument("--trials", type=int, default=3,
                      help="Number of trials to run (default: 3)")
    parser.add_argument("--evolution", action="store_true",
                      help="Use evolution instead of LLM")
    parser.add_argument("--population", type=int, default=100,
                      help="Population size for evolution (default: 100)")
    parser.add_argument("--generations", type=int, default=50,
                      help="Number of generations for evolution (default: 50)")
    
    # Output options
    parser.add_argument("--output-dir", type=str, default="results/single_experiment",
                      help="Directory to save results (default: results/single_experiment)")
    parser.add_argument("--description", type=str, default=None,
                      help="Description of the experiment")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create experiment configuration
    config = ExperimentConfig(
        provider=args.provider,
        model=args.model,
        prompt=args.prompt,
        temperature=args.temperature,
        steps=args.steps,
        trials=args.trials,
        use_evolution=args.evolution,
        population_size=args.population if args.evolution else None,
        generations=args.generations if args.evolution else None,
        description=args.description or f"Single experiment with {args.provider} {args.model}"
    )
    
    # Create results manager
    results_manager = ResultsManager(str(output_dir))
    
    # Create experiment runner
    runner = ExperimentRunner(results_manager)
    
    # Run the experiment
    print(f"\nRunning experiment: {config.description}")
    print(f"Provider: {config.provider}")
    print(f"Model: {config.model}")
    print(f"Prompt: {config.prompt}")
    print(f"Steps: {config.steps}")
    print(f"Trials: {config.trials}")
    if config.use_evolution:
        print(f"Using evolution with population={config.population_size}, generations={config.generations}")
    print()
    
    summary = runner.run_experiment(config)
    
    # Print results
    print("\n===== EXPERIMENT RESULTS =====\n")
    print(f"Average Coverage: {summary.avg_coverage:.2%}")
    print(f"Average Efficiency: {summary.avg_efficiency:.2f}")
    print(f"Average Steps: {summary.avg_steps:.1f}")
    print(f"Average Cells Visited: {summary.avg_cells_visited:.1f}")
    
    if summary.total_cost is not None:
        print(f"Total Cost: ${summary.total_cost:.4f}")
        print(f"Total Tokens: {summary.total_tokens}")
    
    print(f"\nResults saved to {output_dir}")
    print(f"Experiment ID: {summary.experiment_id}")

if __name__ == "__main__":
    main() 