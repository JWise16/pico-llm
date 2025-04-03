# LLM Integration Demo

## Introduction
This demo walks through our findings, challenges, and some fascinating behaviors we've observed while letting LLM's play picbot.

## Demo Flow

### 1. Classic Mode Baseline
```bash
python -m picobot --classic
```
This is our reference point - the traditional rule-based Picobot that we all know and love.

### 2. Evolution Mode Comparison
```bash
python -m picobot --evolve --population 100 --generations 50 --steps 500
```
The genetic algorithm approach gives us interesting insights into this strategy:
- Typically achieves ~90% coverage
- Develops wall-following behaviors organically
- Uses state transitions strategically

### 3. LLM Attempts at Rule Generation

#### OpenAI (GPT-3.5)
```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100
```
Interesting behaviors:
- Tends to generate overly simplistic rules
- Often defaults to basic North-South alternation
- Struggles with pattern format despite explicit instructions

#### Anthropic (Claude)
```bash
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --steps 100
```
Different challenges:
- Attempts more sophisticated strategies but fails in execution
- Often includes explanatory comments (which break parsing)
- Tries to use wildcards (*) instead of 'x'

### 4. Pattern Format Challenge
A fascinating challenge we've encountered is getting LLMs to consistently follow the pattern format:

Expected:
```
0 NExx -> W 1    # Valid: North & East walls
0 xxWS -> N 0    # Valid: West & South walls
```

What we often get:
```
- N*** -> E 0    # Uses wildcards
- N x x x -> N 1 # Adds spaces
State 0: NExx -> W 1  # Adds labels
```

### 5. Strategic Thinking
The LLMs understand the concept of wall-following and state transitions, as seen in their explanations:

```
"Following a right-hand wall strategy in State 0..."
"Using State 1 for corner handling..."
"State 2 handles backtracking from dead ends..."
```

But they struggle to translate this understanding into valid rule syntax.

### 6. Current Workarounds
- Default rules for missing patterns
- Strict validation of rule format
- Pattern cleanup attempts

### 7. Future Directions
- Hybrid approach combining LLM strategy with evolution-based optimization
- More sophisticated prompt engineering
- Potential for learning from successful evolution-generated rules

## Interactive Elements
During the demo, we can:
1. Modify prompts in real-time
2. Compare coverage between different approaches
3. Examine specific rule generation attempts
4. Discuss potential improvements with the Picobot team

## Discussion Points
1. How does LLM rule generation compare to evolution-based approaches?
2. Could we use LLMs to optimize evolution parameters?
3. What makes rule format adherence so challenging for LLMs?
4. How might we better leverage LLMs' strategic understanding? 