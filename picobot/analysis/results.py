"""Classes for storing and managing experiment results."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os
from pathlib import Path

class ExperimentResults(BaseModel):
    """Results from a single experiment trial."""
    
    # Trial metadata
    trial_id: int = Field(..., description="Trial number")
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # Performance metrics
    coverage: float = Field(..., ge=0.0, le=1.0, description="Percentage of grid covered")
    efficiency: float = Field(..., ge=0.0, description="Efficiency metric (cells visited per step)")
    total_steps: int = Field(..., gt=0, description="Total steps taken")
    unique_cells_visited: int = Field(..., gt=0, description="Number of unique cells visited")
    
    # LLM metrics (if applicable)
    llm_metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metrics from LLM usage (tokens, cost, etc.)"
    )
    
    # Evolution metrics (if applicable)
    evolution_metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metrics from evolution (fitness, generations, etc.)"
    )

class TrialResult(BaseModel):
    """Results from a single trial."""
    
    # Trial metadata
    trial_num: int = Field(..., description="Trial number")
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    # Performance metrics
    coverage: float = Field(..., ge=0.0, le=1.0, description="Percentage of grid covered")
    efficiency: float = Field(..., ge=0.0, description="Efficiency metric (cells visited per step)")
    combined_score: float = Field(..., ge=0.0, le=1.0, description="Combined performance score")
    steps: int = Field(..., gt=0, description="Total steps taken")
    cells_visited: int = Field(..., gt=0, description="Number of unique cells visited")
    got_stuck: bool = Field(..., description="Whether the robot got stuck")
    
    # LLM metrics (if applicable)
    llm_metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metrics from LLM usage (tokens, cost, etc.)"
    )

class ExperimentSummary(BaseModel):
    """Summary of all trials for an experiment."""
    
    # Experiment metadata
    experiment_id: str = Field(..., description="ID of the experiment")
    config: Dict[str, Any] = Field(..., description="Experiment configuration")
    
    # Results
    trials: List[ExperimentResults] = Field(default_factory=list)
    
    # Aggregated metrics
    avg_coverage: float = Field(..., ge=0.0, le=1.0)
    avg_efficiency: float = Field(..., ge=0.0)
    avg_steps: float = Field(..., gt=0)
    avg_cells_visited: float = Field(..., gt=0)
    
    # Cost metrics (if applicable)
    total_cost: Optional[float] = Field(default=None)
    total_tokens: Optional[int] = Field(default=None)
    
    def add_trial(self, trial: ExperimentResults) -> None:
        """Add a trial result to the experiment summary."""
        self.trials.append(trial)
        self._update_metrics()
    
    def _update_metrics(self) -> None:
        """Update aggregated metrics based on trial results."""
        if not self.trials:
            return
            
        self.avg_coverage = sum(t.coverage for t in self.trials) / len(self.trials)
        self.avg_efficiency = sum(t.efficiency for t in self.trials) / len(self.trials)
        self.avg_steps = sum(t.total_steps for t in self.trials) / len(self.trials)
        self.avg_cells_visited = sum(t.unique_cells_visited for t in self.trials) / len(self.trials)
        
        # Update LLM metrics if available
        if all(t.llm_metrics for t in self.trials):
            self.total_cost = sum(t.llm_metrics.get("cost", 0) for t in self.trials)
            self.total_tokens = sum(t.llm_metrics.get("total_tokens", 0) for t in self.trials)

class ResultsManager:
    """Manager for saving and loading experiment results."""
    
    def __init__(self, output_dir: str = "results"):
        """Initialize the results manager.
        
        Args:
            output_dir: Directory to store results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_results(self, summary: ExperimentSummary) -> None:
        """Save experiment results to disk.
        
        Args:
            summary: Experiment summary to save
        """
        # Create experiment directory
        exp_dir = self.output_dir / summary.experiment_id
        exp_dir.mkdir(exist_ok=True)
        
        # Save summary
        summary_path = exp_dir / "summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary.model_dump(), f, indent=2, default=str)
        
        # Save individual trials
        trials_dir = exp_dir / "trials"
        trials_dir.mkdir(exist_ok=True)
        
        for trial in summary.trials:
            trial_path = trials_dir / f"trial_{trial.trial_id}.json"
            with open(trial_path, "w") as f:
                json.dump(trial.model_dump(), f, indent=2, default=str)
    
    def load_results(self, experiment_id: str) -> Optional[ExperimentSummary]:
        """Load experiment results from disk.
        
        Args:
            experiment_id: ID of the experiment to load
            
        Returns:
            Experiment summary if found, None otherwise
        """
        exp_dir = self.output_dir / experiment_id
        if not exp_dir.exists():
            return None
            
        # Load summary
        summary_path = exp_dir / "summary.json"
        if not summary_path.exists():
            return None
            
        with open(summary_path) as f:
            data = json.load(f)
            return ExperimentSummary.model_validate(data)
    
    def list_experiments(self) -> List[str]:
        """List all available experiments.
        
        Returns:
            List of experiment IDs
        """
        return [d.name for d in self.output_dir.iterdir() if d.is_dir()]
    
    def get_experiment_path(self, experiment_id: str) -> Path:
        """Get the path to an experiment's directory.
        
        Args:
            experiment_id: ID of the experiment
            
        Returns:
            Path to the experiment directory
        """
        return self.output_dir / experiment_id 