# Picobot LLM Setup and Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Available Modes](#available-modes)
4. [Running Picobot](#running-picobot)
5. [Analysis and Experiments](#analysis-and-experiments)
6. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/jwise16/pico-llm.git
cd pico-llm
```

### Step 2: Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Environment Setup

### API Keys
Create a `.env` file in the root directory with your API keys:
```bash
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Optional for Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Available Modes

### 1. Classic Mode
Traditional rule-based Picobot implementation.

### 2. Evolution Mode
Genetic algorithm-based rule generation.

### 3. LLM Mode
AI language model control and rule generation.

## Running Picobot

### Classic Mode
```bash
python -m picobot --classic
```

### Evolution Mode
```bash
# Basic evolution
python -m picobot --evolve

# Custom parameters
python -m picobot --evolve --population 100 --generations 50 --steps 500
```

### LLM Mode
```bash
# Using OpenAI
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100

# Using Anthropic
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --steps 100

# With custom prompt
python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt wall_following --steps 200
```

### Common Options
- `--steps`: Number of steps to run (default: 500)
- `--fps`: Visualization speed in frames per second (default: 30)
- `--evaluate`: Enable performance evaluation
- `--trials`: Number of trials for evaluation (default: 5)

## Analysis and Experiments

### Running Single Experiments
```bash
# LLM experiment
python -m picobot.analysis.run_single_experiment --provider openai --model gpt-3.5-turbo --steps 100 --trials 2

# Evolution experiment
python -m picobot.analysis.run_single_experiment --provider none --evolution --population 50 --generations 20 --steps 100 --trials 2
```

### Batch Experiments
```bash
# Run multiple experiments in parallel
python -m picobot.analysis.run_batch_experiments --parallel --workers 4
```

### Analyzing Results
```bash
# Generate analysis plots
python -m picobot.analysis.analyze_results --plot

# Print comparison table
python -m picobot.analysis.analyze_results --table
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Verify API keys are set in `.env` file
   - Check environment variables:
     ```bash
     echo $OPENAI_API_KEY
     echo $ANTHROPIC_API_KEY
     ```

2. **Import Errors**
   - Ensure you're in the project root directory
   - Verify virtual environment is activated
   - Check all dependencies are installed

3. **Connection Issues**
   - Check internet connection
   - Verify API keys are valid
   - Try different provider/model

4. **Rule Generation Issues**
   - Check console output for warnings
   - Try different prompt strategies
   - Adjust temperature parameter

### Debugging Tips

1. **Verbose Output**
   ```bash
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100 --verbose
   ```

2. **Quick Testing**
   ```bash
   # Small population, few generations
   python -m picobot --evolve --population 50 --generations 20 --steps 200
   ```

3. **Fast Visualization**
   ```bash
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100 --fps 60
   ```

For more detailed information about each mode, see:
- [Classic Mode Demo](classic_mode_demo.md)
- [Evolution Mode Demo](evolution_mode_demo.md)
- [LLM Mode Demo](llm_mode_demo.md) 