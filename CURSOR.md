# Picobot - Cursor Agent Documentation

This document provides context and guidance for the Cursor agent when working with the Picobot project.

## Project Context

Picobot is a robot simulation that explores a grid-based environment using either genetic algorithms or LLM-based control. The project demonstrates the integration of traditional programming concepts with modern AI capabilities.

## Key Components

### 1. Core Game Logic
- `robot.py`: Contains the `Robot` class that handles movement and state
- `program.py`: Implements the rule-based program system
- `environment.py`: Manages the grid world and wall detection
- `state.py`: Tracks the current state of the robot and its surroundings

### 2. LLM Integration
- `llm/base.py`: Defines the `LLMInterface` abstract base class
- `llm/providers/`: Contains provider-specific implementations
  - `openai.py`: OpenAI GPT integration
  - `anthropic.py`: Anthropic Claude integration

### 3. Evolution System
- `evolution.py`: Implements the genetic algorithm for program evolution
- `constants.py`: Contains evolution parameters and game constants

### 4. Visualization
- `visualizer.py`: Pygame-based visualization system
- `__main__.py`: Entry point with CLI argument handling

## Common Tasks

### Adding New LLM Providers
1. Create a new provider class in `llm/providers/`
2. Implement the `LLMInterface` abstract methods
3. Update `llm/base.py` to include the new provider
4. Add provider-specific configuration in `config/llm_config.py`

### Modifying Evolution Parameters
1. Adjust constants in `constants.py`
2. Update fitness calculation in `evolution.py` if needed
3. Modify visualization parameters in `visualizer.py`

### Debugging Tips
1. Use the `--steps` parameter to control simulation length
2. Enable verbose logging with `--verbose`
3. Check LLM responses in `tests/scenarios/`
4. Use the visualization to debug movement patterns

## Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/scenarios/test_claude.py -v

# Run with coverage
python -m pytest --cov=picobot tests/
```

### Writing Tests
1. Place new tests in `tests/scenarios/`
2. Use pytest fixtures for common setup
3. Include both success and failure cases
4. Test edge cases and boundary conditions

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and returns
- Include docstrings for all classes and methods
- Keep functions focused and single-purpose
- Use meaningful variable names

## Common Issues

### LLM Integration
- Ensure API keys are set in `.env`
- Check response format matches expected JSON structure
- Verify model names are current and supported

### Evolution
- Monitor population diversity
- Adjust mutation rates if stuck in local optima
- Consider increasing trials for better evaluation

### Visualization
- Handle window closing gracefully
- Ensure smooth animation at different speeds
- Support different grid sizes

## Future Considerations

1. Performance Optimization
   - Parallelize evolution trials
   - Cache LLM responses
   - Optimize visualization rendering

2. Feature Additions
   - Support for custom grid layouts
   - Additional LLM providers
   - Advanced visualization options

3. Testing Improvements
   - Add integration tests
   - Implement performance benchmarks
   - Add property-based testing

## Getting Started with Cursor

When working with this project in Cursor:

1. Start by examining the core components in order:
   - `robot.py` and `environment.py` for basic game logic
   - `program.py` for rule-based control
   - `llm/` directory for AI integration
   - `evolution.py` for genetic algorithms

2. Use the test suite to understand expected behavior:
   - `tests/scenarios/` contains integration tests
   - `tests/test_llm.py` for LLM-specific tests
   - `tests/test_anthropic.py` for Claude integration

3. When making changes:
   - Update tests first
   - Make incremental changes
   - Run tests after each change
   - Update documentation as needed

4. Common Cursor Commands:
   - Use semantic search for finding relevant code
   - Use grep search for exact matches
   - Use file editing for making changes
   - Use terminal commands for running tests and the application 