"""Picobot class that represents the robot and its environment."""

from typing import List, Tuple
from .constants import ROWS, COLUMNS
from .program import Program

class Cell:
    """A cell in the Picobot environment."""
    def __init__(self):
        self.visited = False

class Picobot:
    """A robot that moves around in a grid world following a program."""
    
    def __init__(self, start_row: int, start_col: int, program: Program):
        """Initialize a Picobot with a starting position and program.
        
        Args:
            start_row: Starting row position
            start_col: Starting column position
            program: Program that defines the robot's behavior
        """
        self.program = program
        self.array: List[List[Cell]] = []
        
        # Initialize the environment
        for _ in range(ROWS):
            row = []
            for _ in range(COLUMNS):
                row.append(Cell())
            self.array.append(row)
        
        self.robot_row = start_row
        self.robot_col = start_col
        self.state = 0  # Start in state 0
        self.array[start_row][start_col].visited = True
        self.num_visited = 1
        self.consecutive_invalid_moves = 0  # Track consecutive invalid moves
        self.max_stuck_steps = 10  # Maximum number of consecutive invalid moves before considering stuck
    
    def step(self) -> bool:
        """Take one step according to the program rules.
        
        Returns:
            bool: True if the step was valid, False if the robot hit a wall
        """
        # Determine the pattern of walls around the robot
        pattern = ""
        
        # Check north wall
        if self.robot_row == 0:
            pattern += "N"
        else:
            pattern += "x"
            
        # Check east wall
        if self.robot_col == COLUMNS - 1:
            pattern += "E"
        else:
            pattern += "x"
            
        # Check west wall
        if self.robot_col == 0:
            pattern += "W"
        else:
            pattern += "x"
            
        # Check south wall
        if self.robot_row == ROWS - 1:
            pattern += "S"
        else:
            pattern += "x"
        
        # Get the move and next state from the program
        move, self.state = self.program.get_move(self.state, pattern)
        
        # Check if the move would take the robot out of bounds
        if (move == "N" and self.robot_row == 0) or \
           (move == "S" and self.robot_row == ROWS - 1) or \
           (move == "E" and self.robot_col == COLUMNS - 1) or \
           (move == "W" and self.robot_col == 0):
            self.consecutive_invalid_moves += 1
            return False
        
        # Update robot position based on move
        if move == "N":
            self.robot_row -= 1
        elif move == "E":
            self.robot_col += 1
        elif move == "W":
            self.robot_col -= 1
        else:  # move == "S"
            self.robot_row += 1
        
        # Check if the move was valid
        if (self.robot_row < 0 or self.robot_row >= ROWS or 
            self.robot_col < 0 or self.robot_col >= COLUMNS):
            self.consecutive_invalid_moves += 1
            return False
        
        # Reset consecutive invalid moves counter if move was valid
        self.consecutive_invalid_moves = 0
        
        # Update visited status
        if not self.array[self.robot_row][self.robot_col].visited:
            self.num_visited += 1
            self.array[self.robot_row][self.robot_col].visited = True
        
        return True
    
    def run(self, steps: int) -> int:
        """Run the program for a given number of steps.
        
        Args:
            steps: Number of steps to run
            
        Returns:
            int: Number of steps actually taken before termination
        """
        steps_taken = 0
        for _ in range(steps):
            self.step()
            steps_taken += 1
            
            # Check if robot is stuck
            if self.consecutive_invalid_moves >= self.max_stuck_steps:
                print(f"\nRobot appears to be stuck after {steps_taken} steps. Terminating simulation.")
                break
                
        return steps_taken
    
    def is_stuck(self) -> bool:
        """Check if the robot is stuck.
        
        Returns:
            bool: True if the robot is stuck, False otherwise
        """
        return self.consecutive_invalid_moves >= self.max_stuck_steps
    
    def __repr__(self) -> str:
        """String representation of the current state of the environment."""
        output = ["*" * (COLUMNS + 2)]  # Top wall
        
        for r in range(ROWS):
            row = "*"  # Left wall
            for c in range(COLUMNS):
                if self.robot_row == r and self.robot_col == c:
                    row += "P"  # Robot position
                elif self.array[r][c].visited:
                    row += "."  # Visited cell
                else:
                    row += " "  # Unvisited cell
            row += "*"  # Right wall
            output.append(row)
            
        output.append("*" * (COLUMNS + 2))  # Bottom wall
        return "\n".join(output) 