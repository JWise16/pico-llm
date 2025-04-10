"""LLM-based program for Picobot."""

from typing import Tuple, Dict, Any, Set
from ..program import Program
from .base import LLMInterface
from ..game.state import State
from ..constants import ROWS, COLUMNS

class LLMProgram(Program):
    """Program that uses an LLM provider for decision making."""
    
    def __init__(self, provider: LLMInterface):
        """Initialize the LLM program.
        
        Args:
            provider: The LLM provider to use for decisions
        """
        super().__init__()
        self.provider = provider
        self.current_state = 0  # Keep track of state for compatibility
    
    def get_move(self, state: int, pattern: str) -> Tuple[str, int]:
        """Get the next move from the LLM.
        
        Args:
            state: Current state number (unused for LLM)
            pattern: Current wall pattern
            
        Returns:
            Tuple of (move, next_state)
        """
        # Create a State object for the LLM
        llm_state = State(
            position=(self.robot.robot_row, self.robot.robot_col),
            walls=self._pattern_to_walls(pattern),
            visited=self._get_visited_set(),
            steps=self.robot.num_visited
        )
        
        # Get move from LLM
        response = self.provider.get_next_move(llm_state)
        
        # Convert move to proper format and keep same state
        move = response["move"]
        if move in ["North", "N"]:
            move = "N"
        elif move in ["South", "S"]:
            move = "S"
        elif move in ["East", "E"]:
            move = "E"
        elif move in ["West", "W"]:
            move = "W"
        else:
            raise ValueError(f"Invalid move from LLM: {move}")
        
        # Check if the move would hit a wall
        if "N" in pattern and move == "N":
            # Try moving east if possible
            if "E" not in pattern:
                return "E", self.current_state
            # Try moving west if possible
            elif "W" not in pattern:
                return "W", self.current_state
            # Try moving south if possible
            elif "S" not in pattern:
                return "S", self.current_state
            # No valid moves, stay in place
            else:
                return "N", self.current_state
                
        elif "S" in pattern and move == "S":
            # Try moving east if possible
            if "E" not in pattern:
                return "E", self.current_state
            # Try moving west if possible
            elif "W" not in pattern:
                return "W", self.current_state
            # Try moving north if possible
            elif "N" not in pattern:
                return "N", self.current_state
            # No valid moves, stay in place
            else:
                return "S", self.current_state
                
        elif "E" in pattern and move == "E":
            # Try moving north if possible
            if "N" not in pattern:
                return "N", self.current_state
            # Try moving south if possible
            elif "S" not in pattern:
                return "S", self.current_state
            # Try moving west if possible
            elif "W" not in pattern:
                return "W", self.current_state
            # No valid moves, stay in place
            else:
                return "E", self.current_state
                
        elif "W" in pattern and move == "W":
            # Try moving north if possible
            if "N" not in pattern:
                return "N", self.current_state
            # Try moving south if possible
            elif "S" not in pattern:
                return "S", self.current_state
            # Try moving east if possible
            elif "E" not in pattern:
                return "E", self.current_state
            # No valid moves, stay in place
            else:
                return "W", self.current_state
        
        return move, self.current_state
    
    def set_robot(self, robot) -> None:
        """Set the robot reference for state access.
        
        Args:
            robot: The Picobot instance
        """
        self.robot = robot
    
    def _pattern_to_walls(self, pattern: str) -> Dict[str, bool]:
        """Convert a wall pattern to a walls dictionary.
        
        Args:
            pattern: Wall pattern string (e.g., 'NExx')
            
        Returns:
            Dictionary of wall presence by direction
        """
        return {
            "N": "N" in pattern,
            "E": "E" in pattern,
            "S": "S" in pattern,
            "W": "W" in pattern
        }
    
    def _get_visited_set(self) -> Set[Tuple[int, int]]:
        """Get the set of visited positions.
        
        Returns:
            Set of (row, col) tuples for visited positions
        """
        visited = set()
        for row in range(len(self.robot.array)):
            for col in range(len(self.robot.array[0])):
                if self.robot.array[row][col].visited:
                    visited.add((row, col))
        return visited 