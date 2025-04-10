# LLM Integration Demo

## Introduction
This demo walks through our findings, challenges, and some fascinating behaviors we've observed while using LLMs to generate rules for Picobot.

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

### 3. LLM Rule Generation

#### OpenAI (GPT-3.5)
```bash
python -m picobot --llm --provider openai --model gpt-3.5-turbo --steps 100
```
Interesting behaviors:
- Generates complete rule sets upfront
- Tends to create systematic exploration patterns
- Sometimes misses edge cases requiring default rules

#### Anthropic (Claude)
```bash
python -m picobot --llm --provider anthropic --model claude-3-opus-20240229 --steps 100
```
Different approaches:
- Creates more comprehensive rule sets
- Often includes better state transition logic
- May generate rules with explanatory comments

### 4. Rule Format Challenge
A fascinating challenge we've encountered is getting LLMs to consistently follow the rule format:

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
The LLMs demonstrate understanding of exploration strategies in their rule generation:

```
"State 0: Basic wall following..."
"State 1: Corner handling..."
"State 2: Backtracking from dead ends..."
```

And they often create rule sets that reflect this understanding:
```
0 NExx -> W 1    # Handle north-east corner
0 NxWx -> E 0    # Follow north wall
1 xExx -> S 2    # Handle east wall
2 xxSx -> W 1    # Backtrack from south wall
```

### 6. Current Solutions
- JSON-based rule generation for better format control
- Automatic validation and correction of rule format
- Default rules for missing patterns
- State machine validation

### 7. Future Directions
- Enhanced prompt engineering for more reliable rule generation
- Hybrid approaches combining LLM-generated rules with evolution-based optimization
- Learning from successful rule sets to improve generation
- Better handling of edge cases and special situations

## Interactive Elements
During the demo, we can:
1. Examine generated rule sets
2. Compare coverage between different approaches
3. Analyze state transition patterns
4. Discuss potential improvements with the Picobot team

## Discussion Points
1. How does LLM rule generation compare to evolution-based approaches?
2. What strategies do LLMs use to create exploration patterns?
3. How can we improve rule format adherence?
4. What makes certain rule sets more effective than others?
5. How can we better leverage LLMs' understanding of exploration strategies? 