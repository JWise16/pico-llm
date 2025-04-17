"""Demo script for evaluating Picobot programs using the scoring mechanism."""

import argparse
import random
from .robot import Picobot
from .program import Program
from .llm.providers.openai import OpenAIProvider
from .llm.providers.anthropic import AnthropicProvider
from .config.llm_config import LLMConfig
from .llm.scoring import ScoreCalculator
from .llm.rule_generator import generate_rules

def main():
    """Main entry point for the Picobot scoring demo."""
    parser = argparse.ArgumentParser(description="Picobot Scoring Demo - Evaluate Picobot programs")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                      help="LLM provider to use (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                      help="Model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--trials", type=int, default=5,
                      help="Number of trials for evaluation (default: 5)")
    parser.add_argument("--steps", type=int, default=200,
                      help="Number of steps per trial (default: 200)")
    parser.add_argument("--prompt", type=str, default="basic",
                      help="Prompt to use for rule generation (default: basic)")
    parser.add_argument("--random", action="store_true",
                      help="Evaluate a random program instead of LLM-generated")
    args = parser.parse_args()
    
    # Initialize the LLM provider if not using random program
    provider = None
    if not args.random:
        config = LLMConfig()
        if args.provider == "openai":
            provider = OpenAIProvider(args.model, temperature=0.7, config=config)
        else:
            provider = AnthropicProvider(args.model, temperature=0.7)
        
        # Initialize the provider
        provider.initialize()
    
    try:
        # Create a program
        if args.random:
            print("\nGenerating random program...")
            program = Program()
            program.randomize()
        else:
            print(f"\nGenerating rules using {args.provider} ({args.model})...")
            program, _ = generate_rules(provider, prompt_name=args.prompt, evaluate=False)
        
        # Print the program
        print("\nProgram rules:")
        print(program)
        
        # Evaluate the program
        print(f"\nEvaluating program with {args.trials} trials and {args.steps} steps per trial...")
        calculator = ScoreCalculator(trials=args.trials, steps_per_trial=args.steps)
        scores = calculator.evaluate_program(program)
        explanation = calculator.get_score_explanation(scores)
        
        print("\nEvaluation results:")
        print(explanation)
        
    finally:
        # Cleanup
        if provider:
            provider.cleanup()

if __name__ == "__main__":
    main() 