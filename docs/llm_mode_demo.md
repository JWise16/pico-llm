# LLM Mode Demo

## LLM Mode Documentation

The LLM (Large Language Model) mode allows Picobot to be controlled by an AI language model by generating a complete set of rules for autonomous operation. This mode is currently in development and has some known limitations.

### Overview

The LLM mode generates a complete set of rules upfront, similar to the classic mode, but using an AI language model to create the rules. The generated rules are then used by the Picobot simulator without further LLM intervention.

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

#### Rule Generation Process

1. The LLM receives a detailed prompt explaining the rule format and requirements
2. It generates a complete set of rules in JSON format
3. The rules are parsed and validated
4. Any missing rules are automatically filled with default behaviors
5. The complete rule set is used by the Picobot simulator

### Known Issues and Limitations

#### Rule Generation

1. **Format Compliance**: The LLM sometimes struggles to consistently generate rules in the exact required format:
   - Rules should be: `STATE PATTERN -> MOVE NEXT_STATE`
   - Example: `0 NExx -> W 1`

2. **Pattern Validation**: Issues with:
   - Incorrect use of wildcards (*) instead of 'x'
   - Adding spaces within patterns
   - Using invalid characters in patterns

3. **Coverage**: The rule generator often fails to provide rules for all possible state-pattern combinations, requiring default rules to be added automatically.

#### Token Limits and Response Handling

The LLM providers are configured with generous token limits (4000 tokens) to accommodate large rule sets. However, in some cases, responses may still be truncated. The system includes several mechanisms to handle this:

1. **Partial Rule Salvaging**: If a response is truncated, the system will attempt to:
   - Identify the last complete rule in the truncated response
   - Reconstruct a valid JSON structure
   - Parse and use the salvaged rules

2. **Debugging Information**: When issues occur, the system provides detailed logging:
   - Raw LLM response
   - Parsed JSON data
   - Any salvage attempts and results
   - Specific rule parsing failures

3. **Token Usage Tracking**: The system tracks token usage for each provider:
   - OpenAI: Tracks input and output tokens separately
   - Anthropic: Tracks total token usage
   - Cost estimates are calculated based on provider-specific rates

If you encounter token limit issues:
1. Check the debug output for the raw response and parsing attempts
2. Consider reducing the number of rules requested if consistently hitting limits
3. Monitor token usage patterns to optimize prompt engineering

### Future Improvements

Planned enhancements:
1. Improved prompt engineering for more reliable rule generation
2. Better validation and error handling for LLM responses
3. Enhanced state machine design for more sophisticated exploration strategies
4. Hybrid approaches combining LLM-generated rules with evolution-based optimization

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

The LLM mode in Picobot demonstrates how large language models can be used to generate a complete set of rules for autonomous operation. Unlike the classic and evolution modes, which rely on predefined rules or genetic algorithms, the LLM mode leverages the capabilities of advanced language models to generate a comprehensive rule set that can be used by the robot to navigate its environment.

## How It Works

1. **Rule Generation**: The LLM is prompted to generate a complete set of rules for Picobot, following a specific format and addressing all possible wall patterns for each state.

2. **Rule Parsing**: The generated rules are parsed from the LLM's response, with robust error handling for various response formats and potential issues.

3. **Rule Validation**: The parsed rules are validated to ensure they follow the correct format and cover all necessary patterns.

4. **Rule Application**: The validated rules are applied to the robot, which then operates autonomously based on these rules.

## Token Limits and Response Handling

The LLM mode includes robust handling of token limits and response issues:

1. **Increased Token Limits**: Both OpenAI and Anthropic providers are configured with higher token limits (4000 tokens) to accommodate the generation of complete rule sets.

2. **Timeout Handling**: If a request times out, the system will automatically retry with a smaller token limit (2000 tokens) to improve the chances of a successful response.

3. **Partial Rule Salvaging**: If the response is truncated or malformed, the system attempts to salvage partial rules from the response, using multiple strategies:
   - Finding the last complete rule in the truncated response
   - Extracting individual rules using regex patterns
   - Attempting to parse incomplete JSON structures

4. **Debugging Information**: Detailed logging is provided throughout the process, including:
   - Raw LLM responses
   - Parsed JSON data
   - Extracted rules
   - Any errors encountered during parsing or extraction

5. **Token Usage Tracking**: The system tracks token usage and associated costs for each provider.

## Known Issues and Limitations

1. **Format Compliance**: LLMs may sometimes generate rules that don't strictly follow the required format, such as using wildcards instead of the required characters or adding unnecessary spaces.

2. **Coverage Challenges**: Ensuring complete coverage of all wall patterns for each state can be challenging, as LLMs may prioritize certain patterns over others.

3. **Response Reliability**: LLM responses can be unpredictable, with occasional timeouts or malformed outputs that require the salvage mechanisms to recover.

4. **Token Limits**: Even with increased token limits, very large rule sets may still exceed the limits, requiring the system to fall back to smaller limits or partial rule sets.

## Future Improvements

1. **Better Prompt Engineering**: Refining the prompts to encourage more consistent and complete rule generation.

2. **Validation Strategies**: Implementing more sophisticated validation to ensure rule completeness and correctness.

3. **Hybrid Approaches**: Combining LLM-generated rules with evolution-based optimization to improve performance.

4. **Improved Error Recovery**: Enhancing the salvage mechanisms to handle more edge cases and recover more rules from problematic responses.

## Example Output

Here's an example of the current rule generation output:

```
Raw LLM Response:
{
  "rules": [
    {"state": 0, "pattern": "xxxx", "move": "N", "next_state": 1},
    {"state": 0, "pattern": "Nxxx", "move": "E", "next_state": 0},
    {"state": 0, "pattern": "NExx", "move": "S", "next_state": 0},
    {"state": 0, "pattern": "NxWx", "move": "E", "next_state": 0},
    {"state": 0, "pattern": "xxxS", "move": "N", "next_state": 0},
    {"state": 0, "pattern": "xExS", "move": "N", "next_state": 0},
    {"state": 0, "pattern": "xxWS", "move": "N", "next_state": 0},
    {"state": 0, "pattern": "xExx", "move": "N", "next_state": 0},
    {"state": 0, "pattern": "xxWx", "move": "N", "next_state": 0},
    {"state": 1, "pattern": "xxxx", "move": "E", "next_state": 2},
    {"state": 1, "pattern": "Nxxx", "move": "E", "next_state": 1},
    {"state": 1, "pattern": "NExx", "move": "S", "next_state": 1},
    {"state": 1, "pattern": "NxWx", "move": "E", "next_state": 1},
    {"state": 1, "pattern": "xxxS", "move": "E", "next_state": 1},
    {"state": 1, "pattern": "xExS", "move": "N", "next_state": 1},
    {"state": 1, "pattern": "xxWS", "move": "E", "next_state": 1},
    {"state": 1, "pattern": "xExx", "move": "E", "next_state": 1},
    {"state": 1, "pattern": "xxWx", "move": "E", "next_state": 1},
    {"state": 2, "pattern": "xxxx", "move": "S", "next_state": 3},
    {"state": 2, "pattern": "Nxxx", "move": "S", "next_state": 2},
    {"state": 2, "pattern": "NExx", "move": "S", "next_state": 2},
    {"state": 2, "pattern": "NxWx", "move": "S", "next_state": 2},
    {"state": 2, "pattern": "xxxS", "move": "W", "next_state": 2},
    {"state": 2, "pattern": "xExS", "move": "W", "next_state": 2},
    {"state": 2, "pattern": "xxWS", "move": "W", "next_state": 2},
    {"state": 2, "pattern": "xExx", "move": "S", "next_state": 2},
    {"state": 2, "pattern": "xxWx", "move": "S", "next_state": 2},
    {"state": 3, "pattern": "xxxx", "move": "W", "next_state": 4},
    {"state": 3, "pattern": "Nxxx", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "NExx", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "NxWx", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "xxxS", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "xExS", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "xxWS", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "xExx", "move": "W", "next_state": 3},
    {"state": 3, "pattern": "xxWx", "move": "W", "next_state": 3},
    {"state": 4, "pattern": "xxxx", "move": "N", "next_state": 0},
    {"state": 4, "pattern": "Nxxx", "move": "E", "next_state": 4},
    {"state": 4, "pattern": "NExx", "move": "S", "next_state": 4},
    {"state": 4, "pattern": "NxWx", "move": "E", "next_state": 4},
    {"state": 4, "pattern": "xxxS", "move": "N", "next_state": 4},
    {"state": 4, "pattern": "xExS", "move": "N", "next_state": 4},
    {"state": 4, "pattern": "xxWS", "move": "N", "next_state": 4},
    {"state": 4, "pattern": "xExx", "move": "N", "next_state": 4},
    {"state": 4, "pattern": "xxWx", "move": "N", "next_state": 4}
  ]
}
```

## Troubleshooting

If you encounter issues with the LLM mode, here are some common problems and solutions:

1. **Timeout Errors**: If you see timeout errors, the system will automatically retry with a smaller token limit. If this still fails, try:
   - Checking your internet connection
   - Reducing the complexity of the prompt
   - Using a different model (e.g., switching from GPT-4 to GPT-3.5-Turbo)

2. **Malformed Responses**: If the LLM generates malformed responses, the system will attempt to salvage partial rules. Check the debug output to see what rules were successfully extracted.

3. **Incomplete Rule Sets**: If the generated rule set is incomplete, you may need to:
   - Adjust the prompt to emphasize completeness
   - Increase the token limit (if not already at maximum)
   - Consider using a more capable model

4. **Token Limit Issues**: If you consistently hit token limits:
   - Check the debug output to see the token usage
   - Consider reducing the number of rules requested
   - Look for patterns in the token usage to identify potential optimizations

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
5. The complete rule set is used by the Picobot simulator

### Rule Format
Each rule follows the format: `STATE PATTERN -> MOVE NEXT_STATE`
- `STATE`: Current state (0-4)
- `PATTERN`: 4-character string representing walls (N, E, S, W, x)
- `MOVE`: Direction to move (N, E, S, W)
- `NEXT_STATE`: Next state (0-4)

Example rules:
```
0 NExx -> W 4
0 NxWx -> E 0
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
0 NExx -> W 4    # North-east corner, move west to state 4
0 NxWx -> E 0    # North-west wall, move east staying in state 0
1 xExx -> S 2    # East wall, move south to state 2
2 xxSx -> W 1    # South wall, move west to state 1
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