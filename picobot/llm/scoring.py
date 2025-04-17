"""Scoring mechanism for LLM-based Picobot programs."""

from typing import Dict, Any, List, Tuple
from ..robot import Picobot
from ..constants import ROWS, COLUMNS
import random

class ScoreCalculator:
    """Calculator for scoring LLM-based Picobot programs."""
    
    def __init__(self, trials: int = 5, steps_per_trial: int = 200):
        """Initialize the score calculator.
        
        Args:
            trials: Number of trials to run for evaluation
            steps_per_trial: Number of steps per trial
        """
        self.trials = trials
        self.steps_per_trial = steps_per_trial
        self.total_cells = ROWS * COLUMNS
    
    def evaluate_program(self, program) -> Dict[str, float]:
        """Evaluate a program by running multiple trials.
        
        Args:
            program: The program to evaluate
            
        Returns:
            Dictionary containing various scores
        """
        total_coverage = 0
        total_efficiency = 0
        total_steps = 0
        stuck_count = 0
        
        for trial in range(self.trials):
            # Start from a random position
            start_row = random.randint(0, ROWS - 1)
            start_col = random.randint(0, COLUMNS - 1)
            
            # Create a new robot with the program
            robot = Picobot(start_row, start_col, program)
            
            # Run the robot for the specified number of steps
            steps_taken = robot.run(self.steps_per_trial)
            
            # Check if the robot got stuck
            if robot.is_stuck():
                stuck_count += 1
                print(f"Trial {trial+1}: Robot got stuck after {steps_taken} steps")
            
            # Calculate scores for this trial
            coverage = self._calculate_coverage(robot)
            efficiency = self._calculate_efficiency(robot, steps_taken)
            
            total_coverage += coverage
            total_efficiency += efficiency
            total_steps += robot.num_visited
        
        # Calculate average scores
        avg_coverage = total_coverage / self.trials
        avg_efficiency = total_efficiency / self.trials
        
        # Calculate combined score (weighted average)
        combined_score = (0.7 * avg_coverage) + (0.3 * avg_efficiency)
        
        # Apply penalty for getting stuck
        stuck_penalty = (stuck_count / self.trials) * 0.2  # 20% penalty if all trials got stuck
        combined_score = combined_score * (1 - stuck_penalty)
        
        return {
            "coverage": avg_coverage,
            "efficiency": avg_efficiency,
            "combined": combined_score,
            "total_steps": total_steps,
            "stuck_count": stuck_count,
            "stuck_percentage": stuck_count / self.trials
        }
    
    def _calculate_coverage(self, robot: Picobot) -> float:
        """Calculate the coverage score (fraction of cells visited).
        
        Args:
            robot: The Picobot instance
            
        Returns:
            Coverage score between 0 and 1
        """
        return robot.num_visited / self.total_cells
    
    def _calculate_efficiency(self, robot: Picobot, steps_taken: int) -> float:
        """Calculate the efficiency score (unique cells visited per step).
        
        Args:
            robot: The Picobot instance
            steps_taken: Number of steps actually taken
            
        Returns:
            Efficiency score between 0 and 1
        """
        # If no steps were taken, return 0
        if steps_taken == 0:
            return 0
        
        # Calculate how many unique cells were visited per step
        unique_per_step = robot.num_visited / steps_taken
        
        # Normalize to a 0-1 scale (assuming perfect efficiency would be 1.0)
        # This is a heuristic - adjust as needed
        return min(unique_per_step, 1.0)
    
    def get_score_explanation(self, scores: Dict[str, float]) -> str:
        """Generate a human-readable explanation of the scores.
        
        Args:
            scores: Dictionary of scores from evaluate_program
            
        Returns:
            String explanation of the scores
        """
        coverage_percent = scores["coverage"] * 100
        efficiency_percent = scores["efficiency"] * 100
        combined_percent = scores["combined"] * 100
        stuck_percent = scores["stuck_percentage"] * 100
        
        explanation = (
            f"Program Performance:\n"
            f"- Coverage: {coverage_percent:.1f}% of the grid was visited\n"
            f"- Efficiency: {efficiency_percent:.1f}% (unique cells visited per step)\n"
            f"- Combined Score: {combined_percent:.1f}%\n"
            f"- Total cells visited across all trials: {scores['total_steps']}\n"
            f"- Got stuck in {scores['stuck_count']} out of {self.trials} trials ({stuck_percent:.1f}%)"
        )
        
        return explanation 