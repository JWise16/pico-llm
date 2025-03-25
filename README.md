# Picobot

A modern Python 3 implementation of Picobot, a robot that learns to explore its environment using either genetic algorithms or Large Language Models (LLMs). This is a recreation of a classic educational game that demonstrates programming concepts, evolutionary algorithms, and AI-driven decision making.

## Overview

Picobot is a simple robot that moves around in a grid world, trying to explore as much of the space as possible. The robot can follow either a set of rules (program) that determine its movement based on its current state and the pattern of walls around it, or use an LLM to make intelligent decisions about its movement.

### Key Features

- **Grid-based Environment**: A 20x20 grid with walls on all sides
- **Multiple Control Methods**:
  - **State Machine**: Programs use up to 5 states to control robot behavior
  - **LLM-based Control**: Uses OpenAI's GPT models or Anthropic's Claude for intelligent decision making
- **Pattern Matching**: Robot responds to patterns of walls in its immediate vicinity
- **Genetic Algorithm**: Evolves programs to find optimal exploration strategies
- **Modern Visualization**: Real-time visualization using Pygame
- **Type Hints**: Full Python type annotations for better code clarity
- **Modular Design**: Clean separation of game logic, visualization, evolution, and LLM integration

### How It Works

1. **Program Structure** (Genetic Algorithm Mode):
   - Each program consists of rules mapping (state, pattern) → (move, next_state)
   - States are numbers from 0 to 4 (MAX_STATES - 1)
   - Patterns represent walls around the robot (e.g., "Nxxx" means a wall to the north)
   - Moves are one of ["N", "E", "W", "S"]

2. **LLM-based Control**:
   - Supports multiple LLM providers (OpenAI GPT and Anthropic Claude)
   - Uses structured JSON responses for consistent move generation
   - Provides context about current state and environment
   - Includes confidence scoring and reasoning for each move
   - Handles wall avoidance and exploration optimization

3. **Genetic Algorithm**:
   - Creates a population of random programs
   - Evaluates fitness by running multiple trials from random starting positions
   - Selects top programs for reproduction
   - Creates new programs through crossover and mutation
   - Repeats for multiple generations

4. **Visualization**:
   - Green square: Current robot position
   - Gray squares: Visited cells
   - Blue squares: Walls
   - White squares: Unvisited cells

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

### Running with a Random Program (Genetic Algorithm Mode)

To run the game with a random program:
```bash
python -m picobot
```

This will:
1. Generate a random program
2. Display the program's rules
3. Show a visualization of the robot exploring the environment

### Running with LLM Control

To run the game with LLM-based control:
```bash
python -m picobot --llm
```

This will:
1. Initialize the LLM provider (OpenAI by default)
2. Use the LLM to make movement decisions
3. Show a visualization of the robot exploring the environment

#### LLM Options
- `--model`: Specify the LLM model to use (default: "gpt-3.5-turbo" or "claude-3-7-sonnet-20250219")
- `--temperature`: Set the temperature for LLM responses (default: 0.7)
- `--provider`: Choose the LLM provider ("openai" or "anthropic")

### Evolving a Program

To evolve a program using genetic algorithms:
```bash
python -m picobot --evolve
```

#### Command Line Options

- `--evolve`: Enable evolution mode
- `--population`: Population size for evolution (default: 100)
- `--generations`: Number of generations to evolve (default: 50)
- `--steps`: Number of steps to run visualization (default: 500)

#### Example Usage

Run with Anthropic's Claude:
```bash
python -m picobot --llm --provider anthropic --model claude-3-7-sonnet-20250219
```

Run with OpenAI's GPT-4:
```bash
python -m picobot --llm --provider openai --model gpt-4
```

Run evolution with larger population and more generations:
```bash
python -m picobot --evolve --population 200 --generations 100
```

Run with more steps to see longer exploration:
```bash
python -m picobot --evolve --steps 1000
```

### Controls

- Press ESC to exit the visualization
- Close the window to stop the program

## Configuration

### Genetic Algorithm Parameters

The evolution process can be tuned using these parameters in `constants.py`:

- `MAX_STATES`: Maximum number of states in a program (default: 5)
- `TRIALS`: Number of trials to evaluate each program (default: 20)
- `STEPS`: Number of steps per trial (default: 800)
- `MUTATION_RATE`: Probability of mutation (default: 0.02)
- `TOP_FRACTION`: Fraction of population selected for reproduction (default: 0.2)

### LLM Configuration

LLM settings can be configured in `config/llm_config.py`:

- Model selection and parameters
- API timeouts and retry settings
- Cost tracking and token limits
- Provider-specific settings

## Project Structure

```
picobot/
├── __main__.py      # Main entry point
├── constants.py     # Game configuration
├── program.py       # Program class and rules
├── robot.py         # Picobot and environment
├── visualizer.py    # Pygame visualization
├── evolution.py     # Genetic algorithm
├── config/         # Configuration files
│   └── llm_config.py  # LLM settings
└── llm/            # LLM integration
    ├── base.py     # Base LLM interface
    └── providers/  # LLM providers
        ├── openai.py    # OpenAI implementation
        └── anthropic.py # Anthropic implementation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This is a modern recreation of the original Picobot game, which was created as an educational tool to teach programming and algorithms concepts. The original implementation was written in Python 2 and used turtle graphics for visualization. This version extends the concept by adding LLM-based control capabilities and support for multiple AI providers. 