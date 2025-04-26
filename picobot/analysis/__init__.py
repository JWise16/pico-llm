"""Analysis module for Picobot experiments."""

from .config import ExperimentConfig, BatchConfig
from .results import ExperimentResults, ExperimentSummary, ResultsManager
from .runner import ExperimentRunner

__all__ = [
    'ExperimentConfig',
    'BatchConfig',
    'ExperimentResults',
    'ExperimentSummary',
    'ResultsManager',
    'ExperimentRunner'
] 