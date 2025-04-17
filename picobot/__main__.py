"""Main script to run the Picobot game."""

import random
import argparse
from .program import Program
from .robot import Picobot
from .visualizer import Visualizer
from .evolution import evolve
from .llm.providers.openai import OpenAIProvider
from .llm.providers.anthropic import AnthropicProvider
from .config.llm_config import LLMConfig
from .llm.rule_generator import generate_rules
from .llm.prompts import AVAILABLE_PROMPTS
from .llm.scoring import ScoreCalculator

def main():
    """Main entry point for the Picobot game."""
    parser = argparse.ArgumentParser(description="Picobot - A robot that learns to explore its environment")
    parser.add_argument("--evolve", action="store_true", help="Evolve a program using genetic algorithms")
    parser.add_argument("--llm", action="store_true", help="Use LLM to generate rules")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                      help="LLM provider to use (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                      help="Model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--prompt", type=str, choices=list(AVAILABLE_PROMPTS.keys()), default="basic",
                      help="Prompt strategy to use (default: basic)")
    parser.add_argument("--population", type=int, default=100, help="Population size for evolution")
    parser.add_argument("--generations", type=int, default=50, help="Number of generations to evolve")
    parser.add_argument("--steps", type=int, default=500, help="Number of steps to run visualization")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate the program's performance")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials for evaluation")
    args = parser.parse_args()
    
    if args.llm:
        # Initialize LLM provider
        if args.provider == "openai":
            provider = OpenAIProvider(model_name=args.model)
        else:
            provider = AnthropicProvider(model_name=args.model)
        
        # Initialize the provider
        provider.initialize()
        
        try:
            print(f"\nGenerating rules using {args.provider} ({args.model}) with {args.prompt} prompt...")
            program, evaluation_results = generate_rules(provider, prompt_name=args.prompt, evaluate=args.evaluate)
            print("\nGenerated Rules:")
            print(program)
            
            # Create a Picobot with the generated rules
            row = random.randint(0, 19)
            col = random.randint(0, 19)
            picobot = Picobot(row, col, program)
            
            # Visualize the Picobot
            visualizer = Visualizer()
            steps_taken = visualizer.run(picobot, args.steps)
            print(f"\nSimulation ended after {steps_taken} steps")
            
            # Print metrics
            metrics = provider.get_usage_metrics()
            print("\nLLM Metrics:")
            print(f"Total tokens used: {metrics['total_tokens']}")
            print(f"Total cost: ${metrics['cost']:.4f}")
            
            # Evaluate the program if requested
            if args.evaluate:
                print("\nProgram Evaluation:")
                print(evaluation_results["explanation"])
            
        finally:
            # Cleanup
            provider.cleanup()
            
    elif args.evolve:
        # Evolve a program using genetic algorithms
        best_program = evolve(args.population, args.generations)
        program = best_program
    else:
        # Create a random program
        program = Program()
        program.randomize()
        print("Random program:")
        print(program)
    
    if not args.llm:
        # Create a Picobot with the program
        row = random.randint(0, 19)
        col = random.randint(0, 19)
        picobot = Picobot(row, col, program)
        
        # Visualize the Picobot
        visualizer = Visualizer()
        steps_taken = visualizer.run(picobot, args.steps)
        print(f"\nSimulation ended after {steps_taken} steps")
        
        # Evaluate the program if requested
        if args.evaluate:
            print("\nEvaluating program performance...")
            calculator = ScoreCalculator(trials=args.trials, steps_per_trial=200)
            scores = calculator.evaluate_program(program)
            explanation = calculator.get_score_explanation(scores)
            print("\nEvaluation results:")
            print(explanation)
            
            # Print stuck statistics
            if scores.get("stuck_count", 0) > 0:
                print(f"\nStuck Statistics:")
                print(f"Number of trials where robot got stuck: {scores['stuck_count']}")
                print(f"Percentage of trials where robot got stuck: {scores['stuck_percentage']:.1f}%")

if __name__ == "__main__":
    main() 