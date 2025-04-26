# Picobot Analysis Module

This document provides a comprehensive guide to the Picobot analysis module, which is responsible for running experiments, collecting results, and analyzing the performance of different program generation strategies.

## Table of Contents

1. [Overview](#overview)
2. [Key Components](#key-components)
3. [Running Experiments](#running-experiments)
4. [Results Management](#results-management)
5. [Metrics and Evaluation](#metrics-and-evaluation)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Overview

The analysis module provides a framework for:

- Running experiments with different program generation strategies (LLM-based or evolution-based)
- Collecting and analyzing performance metrics
- Saving and loading experiment results
- Comparing different approaches

## Key Components

### ExperimentRunner

The `ExperimentRunner` class is the main entry point for running experiments. It handles:

- Initializing LLM providers or evolution algorithms
- Running trials with different configurations
- Collecting and aggregating results
- Saving results to disk

```python
from picobot.analysis import ExperimentRunner, ExperimentConfig

# Create a runner
runner = ExperimentRunner()

# Create a configuration
config = ExperimentConfig(
    provider="openai",
    model="gpt-3.5-turbo",
    prompt="basic",
    steps=100,
    trials=3
)

# Run the experiment
summary = runner.run_experiment(config)
```

### ExperimentConfig

The `ExperimentConfig` class defines the parameters for an experiment:

```python
from picobot.analysis import ExperimentConfig

config = ExperimentConfig(
    # Experiment metadata
    experiment_id="my_experiment",  # Optional, auto-generated if not provided
    description="Testing GPT-3.5 with basic prompt",  # Optional
    
    # LLM configuration
    provider="openai",  # "openai", "anthropic", or "none"
    model="gpt-3.5-turbo",  # Model name
    prompt="basic",  # Prompt strategy
    temperature=0.7,  # Temperature for generation
    
    # Simulation parameters
    steps=200,  # Number of steps to run
    trials=5,  # Number of trials to run
    
    # Evolution parameters (if using evolution)
    use_evolution=False,  # Whether to use evolution instead of LLM
    population_size=100,  # Population size for evolution
    generations=50,  # Number of generations to evolve
)
```

### ResultsManager

The `ResultsManager` class handles saving and loading experiment results:

```python
from picobot.analysis import ResultsManager

# Create a results manager
results_manager = ResultsManager("results")

# Save results
results_manager.save_results(summary)

# Load results
loaded_summary = results_manager.load_results("my_experiment")

# List available experiments
experiments = results_manager.list_experiments()
```

### Results Classes

The analysis module includes several classes for storing results:

- `TrialResult`: Results from a single trial
- `ExperimentResults`: Results from a single experiment trial (compatible with `ExperimentSummary`)
- `ExperimentSummary`: Summary of all trials for an experiment

## Running Experiments

### Command Line Interface

The easiest way to run experiments is using the command-line interface:

```bash
# Run with OpenAI GPT-3.5
python -m picobot.analysis.run_single_experiment --provider openai --model gpt-3.5-turbo --prompt basic --steps 100 --trials 2

# Run with evolution
python -m picobot.analysis.run_single_experiment --provider none --evolution --population 50 --generations 20 --steps 100 --trials 2
```

### Programmatic Interface

You can also run experiments programmatically:

```python
from picobot.analysis import ExperimentRunner, ExperimentConfig, ResultsManager

# Create a results manager
results_manager = ResultsManager("results")

# Create a runner
runner = ExperimentRunner(results_manager)

# Create a configuration
config = ExperimentConfig(
    provider="openai",
    model="gpt-3.5-turbo",
    prompt="basic",
    steps=100,
    trials=2
)

# Run the experiment
summary = runner.run_experiment(config)

# Print results
print(f"Average Coverage: {summary.avg_coverage:.2%}")
print(f"Average Efficiency: {summary.avg_efficiency:.2f}")
print(f"Average Steps: {summary.avg_steps:.1f}")
print(f"Average Cells Visited: {summary.avg_cells_visited:.1f}")
```

### Batch Experiments

You can run multiple experiments in batch:

```python
from picobot.analysis import BatchConfig, ExperimentConfig

# Create a batch configuration
batch_config = BatchConfig(
    output_dir="results/batch",
    parallel=True,
    max_workers=4
)

# Add experiments
batch_config.add_experiment(ExperimentConfig(
    provider="openai",
    model="gpt-3.5-turbo",
    prompt="basic",
    steps=100,
    trials=2
))

batch_config.add_experiment(ExperimentConfig(
    provider="anthropic",
    model="claude-3-opus-20240229",
    prompt="basic",
    steps=100,
    trials=2
))

# Run the batch
runner = ExperimentRunner()
results = runner.run_batch(batch_config)
```

## Results Management

### Saving Results

Results are automatically saved after each trial if a `ResultsManager` is provided to the `ExperimentRunner`:

```python
from picobot.analysis import ExperimentRunner, ExperimentConfig, ResultsManager

# Create a results manager
results_manager = ResultsManager("results")

# Create a runner with the results manager
runner = ExperimentRunner(results_manager)

# Run the experiment
summary = runner.run_experiment(config)
```

### Loading Results

You can load previously saved results:

```python
from picobot.analysis import ResultsManager

# Create a results manager
results_manager = ResultsManager("results")

# Load results
summary = results_manager.load_results("my_experiment")

# Print results
print(f"Average Coverage: {summary.avg_coverage:.2%}")
print(f"Average Efficiency: {summary.avg_efficiency:.2f}")
```

### Listing Experiments

You can list all available experiments:

```python
from picobot.analysis import ResultsManager

# Create a results manager
results_manager = ResultsManager("results")

# List experiments
experiments = results_manager.list_experiments()
print("Available experiments:")
for exp_id in experiments:
    print(f"  - {exp_id}")
```

## Metrics and Evaluation

### Performance Metrics

The analysis module tracks several performance metrics:

- **Coverage**: Percentage of the grid covered by the robot
- **Efficiency**: Cells visited per step
- **Steps**: Number of steps taken
- **Cells Visited**: Number of unique cells visited
- **Got Stuck**: Whether the robot got stuck

### LLM Metrics

When using LLM-based program generation, the following metrics are tracked:

- **Total Tokens**: Total number of tokens used
- **Total Cost**: Total cost of the API calls

### Evolution Metrics

When using evolution-based program generation, the following metrics are tracked:

- **Fitness**: Fitness score of the best program
- **Generations**: Number of generations evolved

## Advanced Usage

### Custom Metrics

You can extend the `TrialResult` class to include custom metrics:

```python
from picobot.analysis.results import TrialResult
from pydantic import Field

class CustomTrialResult(TrialResult):
    """Extended trial result with custom metrics."""
    
    # Custom metrics
    custom_metric: float = Field(..., description="Custom metric")
```

### Custom Evaluation

You can implement custom evaluation logic by extending the `ExperimentRunner` class:

```python
from picobot.analysis import ExperimentRunner

class CustomExperimentRunner(ExperimentRunner):
    """Extended experiment runner with custom evaluation."""
    
    def _run_trial(self, config, trial_num):
        # Run the trial
        result = super()._run_trial(config, trial_num)
        
        # Add custom evaluation
        result.custom_metric = self._calculate_custom_metric(result)
        
        return result
    
    def _calculate_custom_metric(self, result):
        # Implement custom metric calculation
        return result.coverage * result.efficiency
```

## Troubleshooting

### Common Issues

#### Robot Gets Stuck

If the robot gets stuck after a few steps, it may be due to:

- Invalid program rules
- Insufficient steps to explore the environment
- Unfavorable starting position

Try:
- Increasing the number of steps
- Using a different prompt
- Running more trials

#### LLM API Errors

If you encounter LLM API errors:

- Check your API keys
- Verify your internet connection
- Try a different model or provider

#### Evolution Not Converging

If evolution is not producing good results:

- Increase the population size
- Increase the number of generations
- Adjust the fitness function

### Debugging

To enable more verbose output, you can modify the logging level:

```python
import logging

# Set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
```

## Conclusion

The analysis module provides a powerful framework for running experiments and analyzing the performance of different program generation strategies. By using the tools and techniques described in this document, you can gain valuable insights into the effectiveness of LLM-based and evolution-based approaches for generating Picobot programs. 