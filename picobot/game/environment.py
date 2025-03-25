from typing import Set, Tuple

class Environment:
    """Class representing the Picobot environment."""
    
    def __init__(self, width: int = 25, height: int = 25):
        """Initialize the environment.
        
        Args:
            width: Width of the environment
            height: Height of the environment
        """
        self.width = width
        self.height = height
        self.walls: Set[Tuple[int, int]] = set()
        
        # Add boundary walls
        for x in range(-1, width + 1):
            self.walls.add((x, -1))
            self.walls.add((x, height))
        for y in range(-1, height + 1):
            self.walls.add((-1, y))
            self.walls.add((width, y))
    
    def set_cell(self, x: int, y: int, is_wall: bool) -> None:
        """Set the state of a cell.
        
        Args:
            x: X coordinate
            y: Y coordinate
            is_wall: True if the cell should be a wall
        """
        if is_wall:
            self.walls.add((x, y))
        else:
            self.walls.discard((x, y))
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if a cell is a wall.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the cell is a wall, False otherwise
        """
        return (x, y) in self.walls
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid (within bounds and not a wall).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the position is valid, False otherwise
        """
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                not self.is_wall(x, y)) 