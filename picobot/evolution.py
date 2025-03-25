"""Genetic algorithm for evolving Picobot programs."""

import random
from typing import List, Tuple
from .constants import (
    MAX_STATES, TRIALS, STEPS, MUTATION_RATE, TOP_FRACTION,
    ROWS, COLUMNS
)
from .program import Program
from .robot import Picobot

def random_population(size: int) -> List[Program]:
    """Create a random population of programs.
    
    Args:
        size: Size of the population
        
    Returns:
        List of random programs
    """
    population = []
    for _ in range(size):
        program = Program()
        program.randomize()
        population.append(program)
    return population

def evaluate_fitness(program: Program, trials: int, trial_length: int) -> float:
    """Evaluate the fitness of a program by running multiple trials.
    
    Args:
        program: Program to evaluate
        trials: Number of trials to run
        trial_length: Number of steps per trial
        
    Returns:
        Average fraction of the room visited (0 to 1)
    """
    total_visited = 0
    
    for _ in range(trials):
        # Start from a random position
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLUMNS - 1)
        picobot = Picobot(row, col, program)
        picobot.run(trial_length)
        total_visited += picobot.num_visited
    
    return (total_visited / trials) / (ROWS * COLUMNS)

def rank(population: List[Program]) -> List[Tuple[float, Program]]:
    """Rank programs by their fitness scores.
    
    Args:
        population: List of programs to rank
        
    Returns:
        List of (score, program) tuples, sorted by score in descending order
    """
    scored = [(evaluate_fitness(program, TRIALS, STEPS), program) 
              for program in population]
    # Sort by the first element (fitness score) in descending order
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored

def evolve(population_size: int, generations: int) -> Program:
    """Evolve a population of programs using genetic algorithms.
    
    Args:
        population_size: Size of the population
        generations: Number of generations to evolve
        
    Returns:
        Best program found
    """
    print(f"Grid size: {ROWS} by {COLUMNS}")
    print(f"Fitness measured using {TRIALS} trials and {STEPS} steps")
    
    current_generation = random_population(population_size)
    
    for gen in range(generations):
        scored = rank(current_generation)
        scores = [score for score, _ in scored]
        
        print(f"\nGeneration {gen}")
        print(f"  Average fitness: {sum(scores) / population_size:.3f}")
        print(f"  Best fitness: {max(scores):.3f}")
        
        # Select top programs for reproduction
        cutoff = int(population_size * TOP_FRACTION)
        best = scored[:cutoff]
        
        # Create next generation
        next_generation = []
        for _ in range(population_size):
            # Select parents from best programs
            parent1 = random.choice(best)[1]
            parent2 = random.choice(best)[1]
            
            # Create offspring through crossover
            offspring = parent1.crossover(parent2)
            
            # Apply mutation
            if random.random() < MUTATION_RATE:
                offspring.mutate()
            
            next_generation.append(offspring)
        
        current_generation = next_generation
    
    # Return the best program from the final generation
    best_program = rank(current_generation)[0][1]
    print("\nBest program found:")
    print(best_program)
    return best_program 