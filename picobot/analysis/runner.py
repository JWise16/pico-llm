"""Experiment runner for executing Picobot experiments."""

from typing import Dict, Any, Optional, List
import random
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from .config import ExperimentConfig, BatchConfig
from .results import ExperimentResults, ExperimentSummary, ResultsManager, TrialResult
from ..robot import Picobot
from ..program import Program
from ..llm.providers import OpenAIProvider, AnthropicProvider
from ..llm.rule_generator import generate_rules
from ..evolution import evolve
from ..llm.scoring import ScoreCalculator
from ..constants import ROWS, COLUMNS

class ExperimentRunner:
    """Runner for executing Picobot experiments."""
    
    def __init__(self, results_manager: Optional[ResultsManager] = None):
        """Initialize the experiment runner.
        
        Args:
            results_manager: Optional results manager for saving results
        """
        self.results_manager = results_manager or ResultsManager()
        self.score_calculator = ScoreCalculator()
        self.llm_provider = None
    
    def run_experiment(self, config: ExperimentConfig) -> ExperimentSummary:
        """Run a single experiment.
        
        Args:
            config: Experiment configuration
            
        Returns:
            Summary of experiment results
        """
        # Initialize LLM provider if needed
        if config.provider != "none":
            self._initialize_llm_provider(config)
        
        # Run first trial to get initial values
        initial_results = self._run_trial(config, 0)
        
        # Convert TrialResult to ExperimentResults
        exp_results = ExperimentResults(
            trial_id=initial_results.trial_num,
            start_time=initial_results.start_time,
            end_time=initial_results.end_time,
            coverage=initial_results.coverage,
            efficiency=initial_results.efficiency,
            total_steps=initial_results.steps,
            unique_cells_visited=initial_results.cells_visited,
            llm_metrics=initial_results.llm_metrics
        )
        
        summary = ExperimentSummary(
            experiment_id=config.experiment_id,
            config=config.model_dump(),
            avg_coverage=initial_results.coverage,
            avg_efficiency=initial_results.efficiency,
            avg_steps=initial_results.steps,
            avg_cells_visited=initial_results.cells_visited
        )
        
        # Add the first trial
        summary.add_trial(exp_results)
        
        # Run remaining trials
        for trial_id in range(1, config.trials):
            trial_results = self._run_trial(config, trial_id)
            
            # Convert TrialResult to ExperimentResults
            exp_results = ExperimentResults(
                trial_id=trial_results.trial_num,
                start_time=trial_results.start_time,
                end_time=trial_results.end_time,
                coverage=trial_results.coverage,
                efficiency=trial_results.efficiency,
                total_steps=trial_results.steps,
                unique_cells_visited=trial_results.cells_visited,
                llm_metrics=trial_results.llm_metrics
            )
            
            summary.add_trial(exp_results)
            
            # Save results after each trial
            if self.results_manager:
                self.results_manager.save_results(summary)
        
        # Clean up LLM provider if needed
        if self.llm_provider:
            self.llm_provider.cleanup()
            self.llm_provider = None
        
        return summary
    
    def _initialize_llm_provider(self, config: ExperimentConfig) -> None:
        """Initialize the LLM provider based on the configuration.
        
        Args:
            config: Experiment configuration
        """
        if config.provider == "openai":
            self.llm_provider = OpenAIProvider(config.model, config.temperature)
        elif config.provider == "anthropic":
            self.llm_provider = AnthropicProvider(config.model, config.temperature)
        else:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")
        
        # Initialize the provider
        self.llm_provider.initialize()
    
    def _generate_program(self, config: ExperimentConfig) -> Program:
        """Generate a program based on the configuration.
        
        Args:
            config: Experiment configuration
            
        Returns:
            Generated program
        """
        if config.use_evolution:
            # Use evolution to generate a program
            population = [Program() for _ in range(config.population_size)]
            for program in population:
                program.randomize()
            
            best_program = evolve(
                population=population,
                generations=config.generations,
                steps=config.steps
            )
            return best_program
        else:
            # Use LLM to generate a program
            if not self.llm_provider:
                self._initialize_llm_provider(config)
            
            program, _ = generate_rules(
                provider=self.llm_provider,
                prompt_name=config.prompt,
                evaluate=False
            )
            return program
    
    def _run_trial(self, config: ExperimentConfig, trial_num: int) -> TrialResult:
        """Run a single trial of the experiment.
        
        Args:
            config: Experiment configuration
            trial_num: Trial number
            
        Returns:
            TrialResult object containing the results
        """
        start_time = datetime.now()
        
        # Generate a program
        program = self._generate_program(config)
        
        # Create Picobot instance with random starting position
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLUMNS - 1)
        picobot = Picobot(row, col, program)
        
        # Run the robot
        steps_taken = picobot.run(config.steps)
        
        # Calculate metrics
        total_cells = ROWS * COLUMNS
        visited_cells = picobot.num_visited
        coverage = visited_cells / total_cells
        efficiency = visited_cells / steps_taken if steps_taken > 0 else 0
        combined_score = (coverage + efficiency) / 2
        
        # Get LLM metrics if applicable
        llm_metrics = None
        if config.provider != "none" and self.llm_provider:
            llm_metrics = self.llm_provider.get_usage_metrics()
        
        # Create trial result
        result = TrialResult(
            trial_num=trial_num,
            start_time=start_time,
            end_time=datetime.now(),
            coverage=coverage,
            efficiency=efficiency,
            combined_score=combined_score,
            steps=steps_taken,
            cells_visited=visited_cells,
            got_stuck=picobot.is_stuck(),
            llm_metrics=llm_metrics
        )
        
        return result
    
    def run_batch(self, batch_config: BatchConfig) -> Dict[str, ExperimentSummary]:
        """Run a batch of experiments.
        
        Args:
            batch_config: Batch configuration
            
        Returns:
            Dictionary mapping experiment IDs to their summaries
        """
        results = {}
        
        if batch_config.parallel:
            with ProcessPoolExecutor(max_workers=batch_config.max_workers) as executor:
                future_to_exp = {
                    executor.submit(self.run_experiment, config): exp_id
                    for exp_id, config in batch_config.experiments.items()
                }
                
                for future in as_completed(future_to_exp):
                    exp_id = future_to_exp[future]
                    try:
                        results[exp_id] = future.result()
                    except Exception as e:
                        print(f"Experiment {exp_id} failed: {str(e)}")
        else:
            for exp_id, config in batch_config.experiments.items():
                try:
                    results[exp_id] = self.run_experiment(config)
                except Exception as e:
                    print(f"Experiment {exp_id} failed: {str(e)}")
        
        return results 