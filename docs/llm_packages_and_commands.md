# LLM Mode Packages and Commands

This document provides an overview of the packages and commands used in the LLM mode demo for Picobot.

## Package Structure

The LLM integration in Picobot is organized into several packages:

### Core LLM Package (`picobot/llm/`)

- **base.py**: Contains the base interfaces and models for LLM integration
  - `LLMInterface`: Abstract base class for LLM providers
  - `Rule`: Model for Picobot rules
  - `LLMResponse`: Model for structured LLM responses

- **prompts.py**: Centralized prompt management
  - `PROMPTS`: Dictionary of available prompts
  - `get_prompt()`: Function to retrieve prompts by name
  - `list_available_prompts()`: Function to list all available prompts

- **rule_generator.py**: Handles rule generation and validation
  - `generate_rules()`: Main function for generating rules from LLM responses
  - Includes validation and default rule generation for missing patterns

- **program.py**: LLM-based program implementation
  - `LLMProgram`: Extends the base Program class for LLM-based decision making

### Provider Implementations (`picobot/llm/providers/`)

- **openai.py**: OpenAI provider implementation
  - `OpenAIProvider`: Implements the `LLMInterface` for OpenAI models
  - Supports GPT-3.5-Turbo and GPT-4

- **anthropic.py**: Anthropic provider implementation
  - `AnthropicProvider`: Implements the `LLMInterface` for Anthropic models
  - Supports Claude 3 Opus and Claude 3 Sonnet

### Prompt Templates (`picobot/llm/prompts/`)

- **basic.py**: Basic exploration strategy prompt
- **wall_following.py**: Wall-following strategy prompt
- **systematic.py**: Systematic exploration strategy prompt

## Command-Line Interface

The LLM mode can be accessed through the Picobot command-line interface:

```bash
python -m picobot --llm [options]
```

### Basic Options

- `--provider`: Specify the LLM provider (openai or anthropic)
- `--model`: Specify the model to use
- `--steps`: Number of steps to run
- `--temperature`: Temperature for response generation (0.0 to 1.0)
- `--prompt`: Specify the prompt to use (basic, wall_following, or systematic)

### Examples

#### OpenAI Provider

```bash
# Basic usage with GPT-3.5-Turbo
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100

# Using GPT-4 with wall-following prompt
python -m picobot --llm --provider openai --model gpt-4 --prompt wall_following --steps 200

# Using GPT-4 with systematic exploration and custom temperature
python -m picobot --llm --provider openai --model gpt-4 --prompt systematic --temperature 0.5 --steps 300
```

#### Anthropic Provider

```bash
# Basic usage with Claude 3 Sonnet
python -m picobot --llm --provider anthropic --model claude-3-sonnet-20240229 --steps 100

# Using Claude 3 Opus with wall-following prompt
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --prompt wall_following --steps 200

# Using Claude 3 Opus with systematic exploration
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --prompt systematic --steps 300
```

## API Usage

The LLM integration can also be used programmatically:

```python
from picobot.llm.providers import OpenAIProvider, AnthropicProvider
from picobot.llm.rule_generator import generate_rules

# Initialize a provider
provider = OpenAIProvider()
provider.initialize(api_key="your-api-key")

# Generate rules
program = generate_rules(provider)

# Use the program with Picobot
picobot = Picobot(program)
picobot.run(steps=100)
```

## Available Prompts

The system includes three specialized prompts:

1. **Basic**: General exploration strategy
   - Focuses on efficient exploration
   - Uses all 5 states (0-4)
   - Covers all wall patterns for each state

2. **Wall Following**: Specialized wall-following strategy
   - Keeps the wall on the right side when possible
   - Turns right when hitting a wall
   - Handles corners and dead ends gracefully

3. **Systematic**: Systematic exploration approach
   - Prioritizes unexplored areas
   - Uses states to remember visited locations
   - Handles dead ends by backtracking

## Token Limits and Response Handling

Both providers are configured with generous token limits (4000 tokens) to accommodate large rule sets. The system includes several mechanisms to handle truncated responses:

1. **Partial Rule Salvaging**: If a response is truncated, the system will attempt to:
   - Identify the last complete rule in the truncated response
   - Reconstruct a valid JSON structure
   - Parse and use the salvaged rules

2. **Rule Validation**: All rules are validated for:
   - Correct pattern format (4 characters, NSEWx only)
   - Valid state numbers (0-4)
   - Valid moves (N, S, E, W)

3. **Default Rules**: For any missing state-pattern combinations, the system automatically adds default rules to ensure complete coverage.

## Metrics and Monitoring

The providers track usage metrics:

```python
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

5. **Import Errors**: If you see import errors, make sure you're using the latest version of the code:
   - The base interface is located in `picobot.llm.base` and providers should import `LLMInterface` from there
   - The `Rule` class is also defined in `picobot.llm.base`, not in a separate `picobot.rules` module
   - If you see errors like `ModuleNotFoundError: No module named 'picobot.llm.providers.base'` or `ModuleNotFoundError: No module named 'picobot.rules'`, check the import statements in the provider files

6. **Environment Setup**: Ensure you have all required dependencies installed:
   ```bash
   pip install openai anthropic pygame
   ```

7. **Running from the Correct Directory**: Make sure you're running the command from the root directory of the project:
   ```bash
   cd /path/to/pico-llm
   python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100
   ```

8. **Code Structure**: The LLM integration has been refactored to use a more modular approach:
   - Base interfaces and models are in `picobot.llm.base`
   - Provider implementations are in `picobot.llm.providers`
   - Prompt templates are in `picobot.llm.prompts`
   - Rule generation logic is in `picobot.llm.rule_generator`

9. **Common Import Paths**:
   - `from picobot.llm.base import LLMInterface, Rule`
   - `from picobot.llm.prompts import get_prompt`
   - `from picobot.llm.rule_generator import generate_rules` 