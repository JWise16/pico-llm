"""Configuration classes for Picobot experiments."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import re

class ExperimentConfig(BaseModel):
    """Configuration for a single experiment."""
    
    # Experiment metadata
    experiment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None
    
    # LLM configuration
    provider: str = Field(..., description="LLM provider (openai or anthropic)")
    model: str = Field(..., description="Model name to use")
    prompt: str = Field(default="basic", description="Prompt strategy to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for generation")
    
    # Simulation parameters
    steps: int = Field(default=200, gt=0, description="Number of steps to run")
    trials: int = Field(default=5, gt=0, description="Number of trials to run")
    
    # Evolution parameters (if using evolution)
    use_evolution: bool = Field(default=False, description="Whether to use evolution instead of LLM")
    population_size: Optional[int] = Field(default=None, description="Population size for evolution")
    generations: Optional[int] = Field(default=None, description="Number of generations to evolve")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Generate a descriptive experiment ID if not provided
        if not data.get('experiment_id'):
            # Create a base name from provider and model
            base_name = f"{self.provider}_{self.model}"
            if self.use_evolution:
                base_name = f"evolution_{self.population_size}_{self.generations}"
            
            # Add prompt and temperature
            name = f"{base_name}_{self.prompt}_t{self.temperature}"
            
            # Add steps and trials
            name = f"{name}_s{self.steps}_n{self.trials}"
            
            # Clean up the name to be filesystem friendly
            name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
            name = re.sub(r'_+', '_', name)
            name = name.strip('_')
            
            # Add timestamp to ensure uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.experiment_id = f"{name}_{timestamp}"
    
    class Config:
        json_schema_extra = {
            "example": {
                "experiment_id": "openai_gpt-4_wall_following_t0.7_s200_n5_20240417_120000",
                "timestamp": "2024-04-17T12:00:00",
                "description": "Testing GPT-4 with wall following strategy",
                "provider": "openai",
                "model": "gpt-4",
                "prompt": "wall_following",
                "temperature": 0.7,
                "steps": 200,
                "trials": 5,
                "use_evolution": False
            }
        }

class BatchConfig(BaseModel):
    """Configuration for running multiple experiments."""
    
    experiments: Dict[str, ExperimentConfig] = Field(default_factory=dict)
    output_dir: str = Field(default="results", description="Directory to save results")
    parallel: bool = Field(default=False, description="Whether to run experiments in parallel")
    max_workers: Optional[int] = Field(default=None, description="Maximum number of parallel workers")
    
    def add_experiment(self, config: ExperimentConfig) -> None:
        """Add an experiment configuration to the batch."""
        self.experiments[config.experiment_id] = config
    
    def remove_experiment(self, experiment_id: str) -> None:
        """Remove an experiment configuration from the batch."""
        if experiment_id in self.experiments:
            del self.experiments[experiment_id]
    
    def get_experiment(self, experiment_id: str) -> Optional[ExperimentConfig]:
        """Get an experiment configuration by ID."""
        return self.experiments.get(experiment_id)
    
    def list_experiments(self) -> Dict[str, str]:
        """Get a list of all experiments with their descriptions."""
        return {
            exp_id: config.description or f"Experiment {exp_id}"
            for exp_id, config in self.experiments.items()
        } 