"""Demo script for running Picobot with LLM control."""

import argparse
import random
from .robot import Picobot
from .visualizer import Visualizer
from .llm.providers.openai import OpenAIProvider
from .llm.providers.anthropic import AnthropicProvider
from .config.llm_config import LLMConfig

def main():
    """Main entry point for the LLM-controlled Picobot demo."""
    parser = argparse.ArgumentParser(description="Picobot LLM Demo - Control Picobot using Large Language Models")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                      help="LLM provider to use (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                      help="Model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--steps", type=int, default=500,
                      help="Number of steps to run (default: 500)")
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
        
    finally:
        # Cleanup
        provider.cleanup()

if __name__ == "__main__":
    main() 