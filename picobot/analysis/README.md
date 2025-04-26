# Picobot Analysis Module

This module provides tools for running experiments with Picobot, collecting results, and analyzing the performance of different models, prompts, and approaches.

## Overview

The analysis module consists of:

1. **Configuration System**: Define experiments with different parameters
2. **Results Storage**: Save and load experiment results
3. **Experiment Runner**: Execute experiments and collect metrics
4. **Analysis Tools**: Visualize and compare results

## Installation

Make sure you have the required dependencies:

```bash
pip install matplotlib numpy pandas tabulate
```

## Usage

### Running Experiments

The `sample_experiments.py` script demonstrates how to run different types of experiments:

```bash
# Run all experiments
python -m picobot.analysis.sample_experiments

# Run only model comparison experiments
python -m picobot.analysis.sample_experiments --type models

# Run only prompt comparison experiments
python -m picobot.analysis.sample_experiments --type prompts

# Run only evolution comparison experiments
python -m picobot.analysis.sample_experiments --type evolution

# Run experiments in parallel
python -m picobot.analysis.sample_experiments --parallel

# Specify number of parallel workers
python -m picobot.analysis.sample_experiments --parallel --workers 4
```

### Analyzing Results

The `analyze_results.py` script provides tools for analyzing and visualizing experiment results:

```bash
# Print a comparison table of all experiments
python -m picobot.analysis.analyze_results --table

# Generate plots comparing experiments
python -m picobot.analysis.analyze_results --plot

# Analyze a specific experiment
python -m picobot.analysis.analyze_results --experiment-id <experiment_id>

# Specify custom directories
python -m picobot.analysis.analyze_results --results-dir custom_results --output-dir custom_output
```

## Programmatic Usage

You can also use the analysis module programmatically in your own scripts:

```python
from picobot.analysis import (
    ExperimentConfig,
    BatchConfig,
    ExperimentRunner,
    ResultsManager
)

# Create an experiment configuration
config = ExperimentConfig(
    provider="openai",
    model="gpt-4",
    prompt="wall_following",
    steps=200,
    trials=5,
    description="Testing GPT-4 with wall following strategy"
)

# Create a batch configuration
batch = BatchConfig()
batch.add_experiment(config)

# Run the experiments
runner = ExperimentRunner()
results = runner.run_batch(batch)

# Access results
for exp_id, summary in results.items():
    print(f"Experiment {exp_id}:")
    print(f"Average coverage: {summary.avg_coverage:.2%}")
    print(f"Average efficiency: {summary.avg_efficiency:.2f}")
    print(f"Total cost: ${summary.total_cost:.4f}")
```

## Results Structure

Experiment results are stored in the following structure:

```
results/
├── <experiment_id>/
│   ├── summary.json
│   └── trials/
│       ├── trial_0.json
│       ├── trial_1.json
│       └── ...
```

Each trial result contains:
- Performance metrics (coverage, efficiency, steps, cells visited)
- LLM metrics (tokens, cost) if applicable
- Evolution metrics if applicable

## Customizing Experiments

You can create custom experiments by modifying the `sample_experiments.py` script or by creating your own scripts using the analysis module's classes.

Example of a custom experiment:

```python
from picobot.analysis import ExperimentConfig, BatchConfig, ExperimentRunner

# Create a custom experiment
config = ExperimentConfig(
    provider="anthropic",
    model="claude-3-opus-20240229",
    prompt="systematic",
    temperature=0.5,
    steps=300,
    trials=10,
    description="Custom experiment with Claude 3 Opus"
)

# Run the experiment
batch = BatchConfig()
batch.add_experiment(config)
runner = ExperimentRunner()
results = runner.run_batch(batch)
``` 