"""Main script to run the Picobot game."""

import random
import argparse
from .program import Program
from .robot import Picobot
from .visualizer import Visualizer
from .evolution import evolve

def main():
    """Main entry point for the Picobot game."""
    parser = argparse.ArgumentParser(description="Picobot - A robot that learns to explore its environment")
    parser.add_argument("--evolve", action="store_true", help="Evolve a program using genetic algorithms")
    parser.add_argument("--population", type=int, default=100, help="Population size for evolution")
    parser.add_argument("--generations", type=int, default=50, help="Number of generations to evolve")
    parser.add_argument("--steps", type=int, default=500, help="Number of steps to run visualization")
    args = parser.parse_args()
    
    if args.evolve:
        # Evolve a program using genetic algorithms
        best_program = evolve(args.population, args.generations)
        program = best_program
    else:
        # Create a random program
        program = Program()
        program.randomize()
        print("Random program:")
        print(program)
    
    # Create a Picobot with the program
    row = random.randint(0, 19)
    col = random.randint(0, 19)
    picobot = Picobot(row, col, program)
    
    # Visualize the Picobot
    visualizer = Visualizer()
    visualizer.run(picobot, args.steps)

if __name__ == "__main__":
    main() 