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
- [Model Performance Analysis](docs/model_performance.md) - Detailed results from testing various Claude models
- [API Reference](docs/api.md)
- [OpenAI Model Test Results](docs/openai_test_results.md) - Detailed analysis of OpenAI model performance and prompt effectiveness

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

## Testing Framework

The project includes a comprehensive testing framework for evaluating LLM performance across different providers and models. The testing infrastructure includes:

### Test Scripts

- `run_tests.sh`: Base script for running all tests
- `run_anthropic_tests.sh`: Tests for Anthropic's Claude models
- `run_claude_tests.sh`: Specific tests for Claude models
- `run_claude_comparison.sh`: Comparative analysis between Claude models
- `run_groq_tests.sh`: Tests for Groq models with parallel execution support

### Test Scenarios

The `tests/scenarios/` directory contains various test files:
- `test_prompt_performance.py`: Base performance testing
- `test_openai_prompt_performance.py`: OpenAI-specific tests
- `test_anthropic_prompt_performance.py`: Anthropic-specific tests
- `test_groq_prompt_performance.py`: Groq-specific tests
- `test_prompt_comparison.py`: Comparative analysis between different prompts
- `test_claude.py`: Claude model-specific tests
- `test_groq.py`: Groq model-specific tests

### Results Processing

- `process_results.py`: Script for processing and analyzing test results
- `visualize_results.py`: Script for visualizing test results
- Results are stored in the `results/` directory with timestamps

### Running Tests

To run tests for a specific provider:

```bash
# Run all tests
./run_tests.sh

# Run Anthropic tests
./run_anthropic_tests.sh

# Run Claude tests
./run_claude_tests.sh

# Run Groq tests (with parallel execution)
./run_groq_tests.sh
```

## GNU Parallel Usage

This project uses GNU Parallel for efficient parallel execution of tests. The `run_groq_tests.sh` script demonstrates this usage:

```bash
# Install GNU Parallel (if not already installed)
brew install parallel  # For macOS
# or
sudo apt-get install parallel  # For Ubuntu/Debian

# Run tests in parallel
parallel -j 2 --halt-on-error 1 run_model_tests ::: "${MODELS[@]}"
```

GNU Parallel is used under the terms of the GNU General Public License version 3 or later. For more information, see the [GNU Parallel documentation](https://www.gnu.org/software/parallel/). 