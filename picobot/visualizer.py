"""Visualization module for Picobot using Pygame."""

import pygame
from typing import Optional
from .constants import (
    CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    BLACK, WHITE, BLUE, GREEN, GRAY
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
        self.draw_cell(self.picobot.robot_row, self.picobot.robot_col, GREEN)
    
    def run(self, picobot: Picobot, steps: int = 500) -> None:
        """Run the visualization with the given Picobot.
        
        Args:
            picobot: Picobot instance to visualize
            steps: Number of steps to run
        """
        self.picobot = picobot
        self.running = True
        step_count = 0
        
        while self.running and step_count < steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.draw_environment()
            pygame.display.flip()
            
            if self.picobot.step():
                step_count += 1
            
            self.clock.tick(FPS)
        
        pygame.quit() 