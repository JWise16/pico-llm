# Picobot LLM Commands

This document provides a comprehensive list of commands for using Picobot with LLM integration. These commands can be copied and pasted directly into your terminal to try out different LLM providers, models, and exploration strategies.

## Prerequisites

Before running any commands, make sure you have:

1. Installed all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API keys as environment variables:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY="your-openai-api-key"
   
   # For Anthropic
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   ```

## Basic Commands

### Running Picobot with LLM

The basic command to run Picobot with LLM integration is:

```bash
python -m picobot --llm [options]
```

### Available Options

- `--provider`: Specify the LLM provider (`openai` or `anthropic`)
- `--model`: Specify the model to use
- `--prompt`: Specify the prompt strategy (`basic`, `wall_following`, or `systematic`)
- `--steps`: Number of steps to run (default: 500)

## OpenAI Provider Commands

### Basic Usage with GPT-3.5-Turbo

```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 200
```

### Using GPT-3.5-Turbo with Wall-Following Strategy

```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt wall_following --steps 200
```

### Using GPT-3.5-Turbo with Systematic Exploration

```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt systematic --steps 200
```

## Anthropic Provider Commands

### Basic Usage with Claude 3 Sonnet

```bash
python -m picobot --llm --provider anthropic --model claude-3-sonnet-20240229 --steps 200
```

### Using Claude 3 Sonnet with Wall-Following Strategy

```bash
python -m picobot --llm --provider anthropic --model claude-3-sonnet-20240229 --prompt wall_following --steps 200
```

### Using Claude 3 Sonnet with Systematic Exploration

```bash
python -m picobot --llm --provider anthropic --model claude-3-sonnet-20240229 --prompt systematic --steps 200
```

## Prompt Strategies

Picobot supports three different prompt strategies:

1. **Basic** (default): General exploration strategy
   ```bash
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt basic --steps 200
   ```

2. **Wall Following**: Specialized wall-following strategy
   ```bash
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt wall_following --steps 200
   ```

3. **Systematic**: Systematic exploration approach
   ```bash
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --prompt systematic --steps 200
   ```

## Step Count Options

You can adjust the number of steps to control how long the simulation runs:

```bash
# Short run (100 steps)
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100

# Medium run (200 steps)
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 200

# Long run (500 steps)
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 500
```

## Programmatic Usage

You can also use the LLM integration programmatically in your Python code:

```python
from picobot.llm.providers import OpenAIProvider, AnthropicProvider
from picobot.llm.rule_generator import generate_rules
from picobot import Picobot

# Initialize a provider
provider = OpenAIProvider(model_name="gpt-3.5-turbo")
provider.initialize()  # Uses environment variable for API key

# Generate rules with a specific prompt strategy
program = generate_rules(provider, prompt_name="wall_following")

# Create a Picobot with random starting position
row = random.randint(0, 19)
col = random.randint(0, 19)
picobot = Picobot(row, col, program)

# Visualize the Picobot
visualizer = Visualizer()
visualizer.run(picobot, steps=200)

# Get usage metrics
metrics = provider.get_usage_metrics()
print(f"Total tokens: {metrics['total_tokens']}")
print(f"Cost: ${metrics['cost']:.4f}")
```

## Troubleshooting

If you encounter issues with the LLM mode:

1. **API Key Issues**: Ensure your API keys are correctly set in the environment:
   ```bash
   # Check if API keys are set
   echo $OPENAI_API_KEY
   echo $ANTHROPIC_API_KEY
   ```

2. **Import Errors**: Make sure you're running the command from the project root directory:
   ```bash
   cd /path/to/pico-llm
   python -m picobot --llm --provider openai --model gpt-3.5-turbo
   ```

3. **Environment Setup**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

4. **Connection Issues**: If you experience connection problems:
   - Check your internet connection
   - Verify your API keys are valid
   - Try running with a different provider or model

5. **Rule Generation**: If the LLM generates invalid rules:
   - The system will automatically add default rules for missing patterns
   - Check the console output for warnings about invalid rules
   - Try a different prompt strategy 