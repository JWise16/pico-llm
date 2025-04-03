# LLM Mode Demo

## LLM Mode Documentation

The LLM (Large Language Model) mode allows Picobot to be controlled by an AI language model, either for real-time decision making or rule generation. This mode is currently in development and has some known limitations.

### Overview

The LLM mode can operate in two ways:
1. Real-time control: The LLM makes decisions about each move based on the current state
2. Rule generation: The LLM generates a complete set of rules for autonomous operation

### Usage

To run Picobot in LLM mode:

```bash
# Using OpenAI
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100

# Using Anthropic
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --steps 100
```

### Configuration

The LLM mode supports the following parameters:
- `--provider`: The LLM provider to use (openai or anthropic)
- `--model`: The specific model to use
- `--steps`: Number of steps to run
- `--temperature`: Temperature for response generation (0.0 to 1.0)

### Technical Details

#### Architecture

The LLM integration consists of:
- Base LLM interface (`LLMInterface`)
- Provider implementations (OpenAI, Anthropic)
- Rule generator for converting LLM output to Picobot rules

#### State Representation

The LLM receives:
- Current position (x, y)
- Surrounding walls (North, South, East, West)
- Visited positions
- Current state number

### Known Issues and Limitations

#### Rule Generation

1. **Format Compliance**: The LLM currently struggles to consistently generate rules in the exact required format:
   - Rules should be: `STATE PATTERN -> MOVE NEXT_STATE`
   - Example: `0 NExx -> W 1`

2. **Pattern Validation**: Issues with:
   - Incorrect use of wildcards (*) instead of 'x'
   - Adding spaces within patterns
   - Using invalid characters in patterns

3. **Coverage**: The rule generator often fails to provide rules for all possible state-pattern combinations, requiring default rules to be added automatically.

#### Real-time Control

1. **Response Format**: The LLM sometimes generates responses that don't strictly follow the required JSON format.
2. **Decision Consistency**: Move decisions may not always follow a coherent strategy across multiple steps.

### Future Improvements

Planned enhancements:
1. Improved prompt engineering for more reliable rule generation
2. Better validation and error handling for LLM responses
3. Implementation of a hybrid approach combining pre-generated rules with real-time adjustments
4. Enhanced state machine design for more sophisticated exploration strategies

### Examples

#### Current Rule Generation Output

```
# Example of current output with issues:
- xxxx -> E, 0    # Invalid format (extra comma)
- N*** -> E 0     # Invalid pattern (uses wildcards)
- N x x x -> N 1  # Invalid pattern (contains spaces)
```

#### Correct Rule Format

```
# Proper rule format:
0 xxxx -> E 0     # No walls, move East, stay in state 0
0 NExx -> W 1     # North and East walls, move West, switch to state 1
1 xxWS -> N 0     # West and South walls, move North, return to state 0
```

### Related Features

- Classic Mode: Traditional rule-based operation
- Evolution Mode: Genetic algorithm for rule generation
- Visualization: Real-time display of LLM-controlled movement

### Contributing

To improve the LLM mode:
1. Test with different prompts and document results
2. Implement additional validation for rule parsing
3. Develop better strategies for handling missing rules
4. Add support for new LLM providers

## Overview
The LLM (Large Language Model) mode demonstrates how artificial intelligence can be used to generate and control Picobot's behavior. This mode uses advanced language models to create exploration strategies and control the robot's movements.

## Running LLM Mode
To run Picobot in LLM mode, use the following command:
```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100
```

Options:
- `--provider`: Choose the LLM provider (openai or anthropic)
- `--model`: Specify the model to use (e.g., gpt-3.5-turbo, gpt-4, claude-3-opus-20240229)
- `--steps`: Number of steps to run the visualization

## How It Works

### Rule Generation
The LLM generates a complete set of rules for Picobot using the following process:
1. The LLM receives a detailed prompt explaining the rule format and requirements
2. It generates rules that cover all possible wall patterns and states
3. The rules are parsed and validated
4. Any missing rules are automatically filled with default behaviors

### Rule Format
Each rule follows the format: `PATTERN STATE->MOVE NEWSTATE`
- `PATTERN`: 4-character string representing walls (N, E, S, W, x)
- `STATE`: Current state (0-4)
- `MOVE`: Direction to move (N, E, S, W)
- `NEWSTATE`: Next state (0-4)

Example rules:
```
NExx 0->W 4
NxWx 0->E 0
```

### State Machine Design
The LLM typically creates a state machine with the following structure:
- State 0: Basic wall following
- State 1: Corner handling
- State 2: Backtracking
- States 3-4: Special case handling

## Visualization Guide

### Colors and Symbols
- Blue: Robot's current position
- Gray: Visited cells
- White: Unvisited cells
- Red: Walls
- Green: Current state number

### Controls
- Close window to exit
- The visualization will automatically stop after the specified number of steps

## Performance Metrics

### Rule Coverage
- Total number of rules generated
- Number of unique wall patterns covered
- Number of states utilized

### Exploration Efficiency
- Coverage percentage (cells visited / accessible cells)
- Steps taken
- Number of unique cells visited

## Tips for Analysis

### Common Patterns
1. Wall Following
   - Rules that keep the robot moving along walls
   - State transitions for corner handling

2. Backtracking
   - Rules that help the robot escape from dead ends
   - State transitions for retracing steps

3. Systematic Exploration
   - Rules that ensure complete coverage
   - State transitions for pattern recognition

### Debugging Tips
1. Check rule completeness
   - Look for missing wall patterns
   - Verify state transitions

2. Analyze exploration patterns
   - Identify inefficient movements
   - Look for potential loops

3. Monitor state usage
   - Track state transitions
   - Identify unused states

## Related Features
- Classic Mode: Compare with traditional Picobot behavior
- Evolution Mode: Compare with genetically evolved solutions
- Custom Rule Sets: Create your own rules for comparison

## Example Analysis

### Sample Rule Set
```
NExx 0->W 4    # North-east corner, move west to state 4
NxWx 0->E 0    # North-west wall, move east staying in state 0
xExx 1->S 2    # East wall, move south to state 2
xxSx 2->W 1    # South wall, move west to state 1
```

This rule set demonstrates:
1. Wall following behavior
2. State transitions for different scenarios
3. Systematic exploration patterns

## Best Practices
1. Start with a small number of steps to verify behavior
2. Gradually increase steps to test long-term performance
3. Compare results with other modes
4. Experiment with different models and providers
5. Analyze the generated rules for efficiency 