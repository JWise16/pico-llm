"""Game state representation for Picobot."""

from typing import Dict, Any, Set, Tuple
from dataclasses import dataclass

@dataclass
class State:
    """Represents the current state of the Picobot game."""
    
    position: Tuple[int, int]  # Current (x, y) position
    walls: Dict[str, bool]  # Dictionary of walls in each direction (N, E, W, S)
    visited: Set[Tuple[int, int]]  # Set of visited positions
    steps: int  # Number of steps taken
    
    def __init__(self, position: Tuple[int, int], walls: Dict[str, bool], visited: Set[Tuple[int, int]], steps: int = 0):
        """Initialize the game state.
        
        Args:
            position: Current (x, y) position
            walls: Dictionary of walls in each direction (N, E, W, S)
            visited: Set of visited positions
            steps: Number of steps taken
        """
        self.position = position
        self.walls = walls
        self.visited = visited
        self.steps = steps
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary format.
        
        Returns:
            Dictionary representation of the state
        """
        return {
            "position": self.position,
            "walls": self.walls,
            "visited": list(self.visited),  # Convert set to list for serialization
            "steps": self.steps
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'State':
        """Create a State instance from a dictionary.
        
        Args:
            data: Dictionary containing state data
            
        Returns:
            New State instance
        """
        return cls(
            position=tuple(data["position"]),
            walls=data["walls"],
            visited=set(map(tuple, data["visited"])),  # Convert list back to set of tuples
            steps=data["steps"]
        )

    def get_surroundings(self) -> Dict[str, bool]:
        """Get the state of surrounding cells.
        
        Returns:
            Dictionary with directions as keys and wall presence as values
        """
        x, y = self.position
        return {
            "North": self.walls["North"],
            "South": self.walls["South"],
            "East": self.walls["East"],
            "West": self.walls["West"]
        }
    
    def can_move(self, direction: str) -> bool:
        """Check if a move in the given direction is valid.
        
        Args:
            direction: Direction to check ("North", "South", "East", "West")
            
        Returns:
            True if the move is valid, False otherwise
        """
        surroundings = self.get_surroundings()
        return not surroundings[direction]
    
    def move(self, direction: str) -> bool:
        """Attempt to move in the given direction.
        
        Args:
            direction: Direction to move ("North", "South", "East", "West")
            
        Returns:
            True if the move was successful, False otherwise
        """
        if not self.can_move(direction):
            return False
            
        x, y = self.position
        if direction == "North":
            self.position = (x, y + 1)
        elif direction == "South":
            self.position = (x, y - 1)
        elif direction == "East":
            self.position = (x + 1, y)
        elif direction == "West":
            self.position = (x - 1, y)
            
        self.visited.add(self.position)
        self.steps += 1
        return True 