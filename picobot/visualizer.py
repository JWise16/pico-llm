"""Visualization module for Picobot using Pygame."""

import pygame
from typing import Optional
from .constants import (
    CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    BLACK, WHITE, BLUE, GREEN, GRAY, RED
)
from .robot import Picobot

class Visualizer:
    """Visualizer for the Picobot game using Pygame."""
    
    def __init__(self):
        """Initialize the Pygame display."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Picobot")
        self.clock = pygame.time.Clock()
        self.running = False
        self.picobot: Optional[Picobot] = None
        self.font = pygame.font.SysFont(None, 24)
    
    def draw_cell(self, row: int, col: int, color: tuple) -> None:
        """Draw a cell at the given position with the specified color.
        
        Args:
            row: Row position
            col: Column position
            color: RGB color tuple
        """
        x = col * CELL_SIZE + CELL_SIZE
        y = row * CELL_SIZE + CELL_SIZE
        pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    
    def draw_walls(self) -> None:
        """Draw the walls of the environment."""
        # Draw top and bottom walls
        for col in range(WINDOW_WIDTH // CELL_SIZE):
            pygame.draw.rect(self.screen, BLUE, 
                           (col * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, BLUE,
                           (col * CELL_SIZE, WINDOW_HEIGHT - CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))
        
        # Draw left and right walls
        for row in range(WINDOW_HEIGHT // CELL_SIZE):
            pygame.draw.rect(self.screen, BLUE,
                           (0, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, BLUE,
                           (WINDOW_WIDTH - CELL_SIZE, row * CELL_SIZE,
                            CELL_SIZE, CELL_SIZE))
    
    def draw_environment(self) -> None:
        """Draw the current state of the environment."""
        if self.picobot is None:
            return
            
        self.screen.fill(WHITE)
        self.draw_walls()
        
        # Draw visited cells
        for row in range(len(self.picobot.array)):
            for col in range(len(self.picobot.array[0])):
                if self.picobot.array[row][col].visited:
                    self.draw_cell(row, col, GRAY)
        
        # Draw robot
        robot_color = RED if self.picobot.is_stuck() else GREEN
        self.draw_cell(self.picobot.robot_row, self.picobot.robot_col, robot_color)
        
        # Draw status text
        status_text = f"Steps: {self.step_count} | Visited: {self.picobot.num_visited}"
        if self.picobot.is_stuck():
            status_text += " | STUCK!"
        
        text_surface = self.font.render(status_text, True, BLACK)
        self.screen.blit(text_surface, (10, 10))
    
    def run(self, picobot: Picobot, steps: int = 500) -> int:
        """Run the visualization with the given Picobot.
        
        Args:
            picobot: Picobot instance to visualize
            steps: Number of steps to run
            
        Returns:
            int: Number of steps actually taken before termination
        """
        self.picobot = picobot
        self.running = True
        self.step_count = 0
        
        while self.running and self.step_count < steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.draw_environment()
            pygame.display.flip()
            
            # Take a step and check if the robot got stuck
            if self.picobot.step():
                self.step_count += 1
            
            # Check if robot is stuck
            if self.picobot.is_stuck():
                print(f"\nRobot appears to be stuck after {self.step_count} steps. Terminating simulation.")
                # Wait a moment to show the stuck state
                pygame.time.wait(1000)
                break
            
            self.clock.tick(FPS)
        
        pygame.quit()
        return self.step_count 