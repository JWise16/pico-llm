# Picobot LLM Integration

An exploration of using Large Language Models to control and generate rules for Picobot, the classic robot programming game.

## Overview

This project investigates how modern LLMs handle the challenge of generating and executing Picobot rules. We've implemented three modes of operation:

1. **Classic Mode**: Traditional rule-based Picobot
2. **Evolution Mode**: Genetic algorithm for rule generation
3. **LLM Mode**: AI language model control and rule generation

## Features

- Integration with multiple LLM providers (OpenAI, Anthropic)
- Real-time visualization of robot movement
- Rule generation and validation
- Coverage analysis and metrics
- Evolution-based optimization

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jwise16/pico-llm/picobot.git
cd picobot
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional
```

## Usage

### Classic Mode
```bash
python -m picobot --classic
```

### Evolution Mode
```bash
python -m picobot --evolve --population 100 --generations 50 --steps 500
```

### LLM Mode
```bash
# Using OpenAI
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100

# Using Anthropic
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --steps 100
```

## Documentation

See the [docs](docs/) directory for detailed documentation:
- [Classic Mode Demo](docs/classic_mode_demo.md)
- [Evolution Mode Demo](docs/evolution_mode_demo.md)
- [LLM Mode Demo](docs/llm_mode_demo.md)
- [LLM Presentation Demo](docs/llm_presentation_demo.md)

## Current Status

The project is actively exploring LLM integration challenges, particularly:
- Pattern format adherence
- Rule generation completeness
- Strategic decision making
- Hybrid approaches with evolution

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This is a modern recreation of the original Picobot game, which was created as an educational tool to teach programming and algorithms concepts. The original implementation was written in Python 2 and used turtle graphics for visualization. This version extends the concept by adding LLM-based control capabilities and support for multiple AI providers. 