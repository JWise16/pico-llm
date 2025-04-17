"""Demo script for running Picobot with LLM control."""

import argparse
import random
from .robot import Picobot
from .visualizer import Visualizer
from .llm.providers.openai import OpenAIProvider
from .llm.providers.anthropic import AnthropicProvider
from .config.llm_config import LLMConfig
from .llm.scoring import ScoreCalculator

def main():
    """Main entry point for the LLM-controlled Picobot demo."""
    parser = argparse.ArgumentParser(description="Picobot LLM Demo - Control Picobot using Large Language Models")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                      help="LLM provider to use (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                      help="Model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--steps", type=int, default=500,
                      help="Number of steps to run (default: 500)")
    parser.add_argument("--evaluate", action="store_true",
                      help="Evaluate the program's performance after running")
    parser.add_argument("--trials", type=int, default=3,
                      help="Number of trials for evaluation (default: 3)")
    args = parser.parse_args()
    
    # Initialize the LLM provider
    config = LLMConfig()
    if args.provider == "openai":
        provider = OpenAIProvider(args.model, temperature=0.7, config=config)
    else:
        provider = AnthropicProvider(args.model, temperature=0.7)
    
    # Initialize the provider
    provider.initialize()
    
    try:
        # Create a Picobot with random starting position
        row = random.randint(0, 19)
        col = random.randint(0, 19)
        picobot = Picobot(row, col, None)  # No program needed for LLM control
        
        # Visualize the Picobot
        visualizer = Visualizer()
        visualizer.run(picobot, args.steps)
        
        # Evaluate the program's performance if requested
        if args.evaluate:
            print("\nEvaluating program performance...")
            calculator = ScoreCalculator(trials=args.trials, steps_per_trial=200)
            scores = calculator.evaluate_program(picobot.program)
            explanation = calculator.get_score_explanation(scores)
            print("\nEvaluation results:")
            print(explanation)
        
    finally:
        # Cleanup
        provider.cleanup()

if __name__ == "__main__":
    main() 