# Picobot Classic Mode Demo

## Overview
Classic mode represents the traditional Picobot implementation where the robot follows a set of rules generated randomly or through evolution. This mode demonstrates basic concepts of finite state machines, pattern matching, and autonomous exploration.

## Running Classic Mode
```bash
# Basic run with default settings
python -m picobot

# Run with custom number of steps
python -m picobot --steps 1000

# Run with visualization speed control (frames per second)
python -m picobot --fps 30
```

## Understanding the Rules
Each rule in the program follows this format:
```
pattern state -> move next_state
```

For example:
```
NExx 0 -> S 3
```
This means:
- If in state `0` and there are walls to the `N`orth and `E`ast (with any conditions to West and South - marked as `x`)
- Then move `S`outh and transition to state `3`

### Pattern Format
The pattern consists of four characters representing walls in NESW order:
- `N`: North wall
- `E`: East wall
- `W`: West wall
- `S`: South wall
- `x`: Don't care (can be either wall or open)

Examples:
- `NExx`: Walls to North and East
- `xxWS`: Walls to West and South
- `xxxx`: No specific wall requirements

### States (0-4)
- The robot can be in one of 5 states (0-4)
- States help the robot maintain context about its previous decisions
- Different states can have different responses to the same pattern

### Valid Moves
- `N`: Move North
- `E`: Move East
- `W`: Move West
- `S`: Move South

## Visualization Guide

### Colors and Symbols
- 🟩 Green Square: Current robot position
- ⬜ White Square: Unvisited cell
- ⬛ Gray Square: Visited cell
- 🟦 Blue Square: Wall

### Controls
- `ESC`: Exit the visualization
- Close window button: Stop the program

## Example Program Analysis

Let's analyze a sample program:
```
NExx 0 -> S 3  # If walls North and East, move South to state 3
xxWS 2 -> N 1  # If walls West and South in state 2, move North to state 1
xxxx 4 -> E 0  # If no walls matter in state 4, move East to state 0
```

This creates behaviors like:
1. Avoiding corners by detecting two adjacent walls
2. Using states to remember previous positions
3. Having default moves when no specific pattern matches

## Performance Metrics
- Coverage: Percentage of accessible cells visited
- Steps: Number of moves made
- States Used: How many of the 5 states were utilized
- Pattern Efficiency: How many patterns were needed for effective exploration

## Tips for Analysis
1. Watch for repeated patterns in movement
2. Notice how state changes affect decisions
3. Observe wall-following behaviors
4. Look for exploration strategies emerging from simple rules

## Common Patterns

### Wall Following
```
Nxxx 0 -> E 0  # Move East when there's a North wall
xxxS 0 -> W 0  # Move West when there's a South wall
```

### Corner Handling
```
NExx 0 -> S 1  # Move South at NE corner
NxWx 0 -> E 1  # Move East at NW corner
```

### Open Space Navigation
```
xxxx 0 -> N 0  # Default to moving North in open spaces
```

## Debugging Tips
1. Watch for robots getting stuck in loops
2. Notice if certain areas are never explored
3. Check if state transitions are creating effective patterns
4. Observe if the robot efficiently handles dead ends

## Related Features
- Evolution Mode: Uses genetic algorithms to evolve better rule sets
- LLM Mode: Compares rule-based behavior with AI decision making
- Custom Maps: Can be used to test specific navigation challenges 