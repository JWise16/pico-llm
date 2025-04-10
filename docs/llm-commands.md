# Picobot LLM Commands

This document provides a comprehensive list of commands for using Picobot with LLM integration. These commands can be copied and pasted directly into your terminal to try out different LLM providers, models, and exploration strategies.

## Prerequisites

Before running any commands, make sure you have:

1. Installed all required dependencies:
   ```bash
   pip install openai anthropic pygame
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

### Common Options

- `--provider`: Specify the LLM provider (openai or anthropic)
- `--model`: Specify the model to use
- `--steps`: Number of steps to run
- `--temperature`: Temperature for response generation (0.0 to 1.0)
- `--prompt`: Specify the prompt to use (basic, wall_following, or systematic)

## OpenAI Provider Commands

### Basic Usage with GPT-3.5-Turbo

```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100
```

### Using GPT-4 with Wall-Following Prompt

```bash
python -m picobot --llm --provider openai --model gpt-4 --prompt wall_following --steps 200
```

### Using GPT-4 with Systematic Exploration

```bash
python -m picobot --llm --provider openai --model gpt-4 --prompt systematic --steps 300
```

### Customizing Temperature

```bash
python -m picobot --llm --provider openai --model gpt-4 --temperature 0.5 --steps 200
```

## Anthropic Provider Commands

### Basic Usage with Claude 3 Sonnet

```bash
python -m picobot --llm --provider anthropic --model claude-3-sonnet-20240229 --steps 100
```

### Using Claude 3 Opus with Wall-Following Prompt

```bash
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --prompt wall_following --steps 200
```

### Using Claude 3 Opus with Systematic Exploration

```bash
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --prompt systematic --steps 300
```

### Customizing Temperature

```bash
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --temperature 0.5 --steps 200
```

## Advanced Usage

### Running with Different Prompts

Picobot supports three different prompts:

1. **Basic**: General exploration strategy
   ```bash
   python -m picobot --llm --provider openai --model gpt-4 --prompt basic --steps 200
   ```

2. **Wall Following**: Specialized wall-following strategy
   ```bash
   python -m picobot --llm --provider openai --model gpt-4 --prompt wall_following --steps 200
   ```

3. **Systematic**: Systematic exploration approach
   ```bash
   python -m picobot --llm --provider openai --model gpt-4 --prompt systematic --steps 200
   ```

### Running with Different Step Counts

You can adjust the number of steps to control how long the simulation runs:

```bash
# Short run
python -m picobot --llm --provider openai --model gpt-4 --steps 50

# Medium run
python -m picobot --llm --provider openai --model gpt-4 --steps 200

# Long run
python -m picobot --llm --provider openai --model gpt-4 --steps 500
```

### Running with Different Temperature Settings

Temperature controls the randomness of the LLM's responses:

```bash
# More deterministic (lower temperature)
python -m picobot --llm --provider openai --model gpt-4 --temperature 0.1 --steps 200

# Balanced (medium temperature)
python -m picobot --llm --provider openai --model gpt-4 --temperature 0.5 --steps 200

# More creative (higher temperature)
python -m picobot --llm --provider openai --model gpt-4 --temperature 0.9 --steps 200
```

## Programmatic Usage

You can also use the LLM integration programmatically in your Python code:

```python
from picobot.llm.providers import OpenAIProvider, AnthropicProvider
from picobot.llm.rule_generator import generate_rules
from picobot import Picobot

# Initialize a provider
provider = OpenAIProvider(model_name="gpt-4", temperature=0.7)
provider.initialize(api_key="your-api-key")  # Or use environment variable

# Generate rules
program = generate_rules(provider)

# Use the program with Picobot
picobot = Picobot(program)
picobot.run(steps=200)

# Get usage metrics
metrics = provider.get_usage_metrics()
print(f"Total tokens: {metrics['total_tokens']}")
print(f"Cost: ${metrics['cost']:.4f}")
```

## Troubleshooting

If you encounter issues with the LLM mode:

1. **API Key Issues**: Ensure your API key is correctly set in the environment or provided to the initialize method.

2. **Token Limit Errors**: If you consistently hit token limits, try:
   - Using a more concise prompt
   - Reducing the number of rules requested
   - Using a model with higher token limits

3. **Format Issues**: If the LLM generates rules in incorrect formats, the system will attempt to salvage partial rules, but you may see warnings in the output.

4. **Connection Issues**: If you experience connection problems, check your internet connection and API key validity.

5. **Import Errors**: If you see import errors, make sure you're using the latest version of the code and running from the correct directory.

6. **Environment Setup**: Ensure you have all required dependencies installed.

7. **Running from the Correct Directory**: Make sure you're running the command from the root directory of the project:
   ```bash
   cd /path/to/pico-llm
   python -m picobot --llm --provider openai --model gpt-4 --steps 200
   ``` 