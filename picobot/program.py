"""Program class for Picobot that defines its behavior rules."""

from typing import Dict, Tuple, List
import random
from .constants import MAX_STATES, VALID_PATTERNS

class Program:
    """A program that defines Picobot's behavior rules."""
    
    def __init__(self):
        """Initialize an empty program."""
        self.rules_dict: Dict[Tuple[int, str], Tuple[str, int]] = {}
    
    def randomize(self) -> None:
        """Create a random program by generating rules for each state and pattern."""
        for state in range(MAX_STATES):
            for pattern in VALID_PATTERNS:
                next_state = random.randint(0, MAX_STATES - 1)
                # Get possible moves by removing wall directions from pattern
                possible_moves = ["N", "E", "W", "S"]
                for char in pattern:
                    if char != "x":
                        possible_moves.remove(char)
                move = random.choice(possible_moves)
                self.rules_dict[(state, pattern)] = (move, next_state)
    
    def get_move(self, state: int, pattern: str) -> Tuple[str, int]:
        """Get the move and next state for a given state and pattern.
        
        Args:
            state: Current state of the program
            pattern: Pattern of walls around the robot
            
        Returns:
            Tuple of (move, next_state)
        """
        return self.rules_dict[(state, pattern)]
    
    def mutate(self) -> None:
        """Mutate the program by replacing one random rule."""
        pattern = random.choice(VALID_PATTERNS)
        start_state = random.randint(0, MAX_STATES - 1)
        possible_moves = ["N", "E", "W", "S"]
        for char in pattern:
            if char != "x":
                possible_moves.remove(char)
        move = random.choice(possible_moves)
        next_state = random.randint(0, MAX_STATES - 1)
        self.rules_dict[(start_state, pattern)] = (move, next_state)
    
    def crossover(self, other: 'Program') -> 'Program':
        """Create a new program by crossing this program with another.
        
        Args:
            other: Another Program to crossover with
            
        Returns:
            A new Program that combines rules from both parents
        """
        new_program = Program()
        cross_point = random.randint(0, MAX_STATES - 1)
        
        for state in range(MAX_STATES):
            for pattern in VALID_PATTERNS:
                if state <= cross_point:
                    new_program.rules_dict[(state, pattern)] = self.rules_dict[(state, pattern)]
                else:
                    new_program.rules_dict[(state, pattern)] = other.rules_dict[(state, pattern)]
        
        return new_program
    
    def __repr__(self) -> str:
        """String representation of the program's rules."""
        output = []
        for (state, pattern), (move, next_state) in sorted(self.rules_dict.items()):
            output.append(f"{pattern} {state} -> {move} {next_state}")
        return "\n".join(output) 