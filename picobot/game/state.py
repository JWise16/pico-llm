from typing import Dict, Tuple
from .environment import Environment

class State:
    """Class representing the current state of the Picobot game."""
    
    def __init__(self, environment: Environment, position: Tuple[int, int] = (0, 0)):
        """Initialize the game state.
        
        Args:
            environment: The game environment
            position: Initial position (x, y)
        """
        self.environment = environment
        self.position = position
        self.visited = set()
        self.visited.add(position)
    
    def get_surroundings(self) -> Dict[str, bool]:
        """Get the state of surrounding cells.
        
        Returns:
            Dictionary with directions as keys and wall presence as values
        """
        x, y = self.position
        return {
            "North": self.environment.is_wall(x, y + 1),
            "South": self.environment.is_wall(x, y - 1),
            "East": self.environment.is_wall(x + 1, y),
            "West": self.environment.is_wall(x - 1, y)
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
        return True 