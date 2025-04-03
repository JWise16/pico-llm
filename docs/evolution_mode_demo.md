# Picobot Evolution Mode Demo

## Overview
Evolution mode uses genetic algorithms to automatically discover effective exploration strategies for Picobot. Starting with a population of random programs, it iteratively improves them through selection, crossover, and mutation to find optimal solutions.

## Running Evolution Mode
```bash
# Basic run with default parameters
python -m picobot --evolve

# Run with custom parameters
python -m picobot --evolve --population 200 --generations 100 --steps 1000
```

### Command Line Options
- `--evolve`: Enable evolution mode
- `--population`: Number of programs in each generation (default: 100)
- `--generations`: Number of generations to evolve (default: 50)
- `--steps`: Number of steps to run visualization (default: 500)

### Common Command Configurations

#### Quick Testing
```bash
# Small population, few generations for quick testing
python -m picobot --evolve --population 50 --generations 20 --steps 200
```
Use this for:
- Testing changes to the evolution algorithm
- Quick validation of new features
- Debugging issues

#### Thorough Evolution
```bash
# Large population, many generations for thorough exploration
python -m picobot --evolve --population 500 --generations 200 --steps 1000
```
Use this for:
- Finding optimal solutions
- Research experiments
- Production-ready program generation

#### Balanced Performance
```bash
# Medium settings for balanced performance
python -m picobot --evolve --population 200 --generations 100 --steps 500
```
Use this for:
- Regular development testing
- Comparing different strategies
- General exploration

#### Fast Visualization
```bash
# Quick visualization of best program
python -m picobot --evolve --population 100 --generations 50 --steps 100
```
Use this for:
- Demonstrating results
- Quick visual verification
- Teaching/learning purposes

#### Research Configuration
```bash
# High population for genetic diversity
python -m picobot --evolve --population 1000 --generations 300 --steps 800
```
Use this for:
- Academic research
- Algorithm comparison
- Deep exploration of solution space

### Configuration Tips
1. Population Size vs. Generations
   - Larger population + fewer generations = more parallel exploration
   - Smaller population + more generations = deeper refinement
   - Balance based on available computational resources

2. Steps for Visualization
   - More steps = longer observation time
   - Fewer steps = faster iteration
   - Adjust based on program complexity

3. Resource Considerations
   - Memory usage scales with population size
   - CPU usage scales with generations × population
   - Visualization time scales with steps

## How Evolution Works

### 1. Initialization
- Creates a population of random programs
- Each program has up to 5 states (0-4)
- Rules are randomly generated for each state and pattern

### 2. Fitness Evaluation
- Each program is evaluated using multiple trials
- Default: 20 trials from random starting positions
- Each trial runs for 800 steps
- Fitness is calculated as: `visited_cells / accessible_cells`

### 3. Selection
- Top programs are selected based on fitness
- Default: Top 20% of population (TOP_FRACTION = 0.2)
- Tournament selection for diversity

### 4. Reproduction
- Selected programs create offspring through:
  - Crossover: Combining rules from two parents
  - Mutation: Random changes to rules (MUTATION_RATE = 0.02)
- New population replaces old one

### 5. Iteration
- Process repeats for specified generations
- Best program is preserved across generations

## Understanding the Output

### Progress Display
```
Generation 0
  Average fitness: 0.065
  Best fitness: 0.534

Generation 1
  Average fitness: 0.094
  Best fitness: 0.875
```

- Shows improvement over generations
- Average fitness indicates population quality
- Best fitness shows peak performance

### Final Program
```
Best program found:
NExx 0 -> W 4
NxWx 0 -> E 0
...
```

- Complete set of rules for best program
- Uses all available states
- Handles all possible wall patterns

## Performance Analysis

### Typical Evolution Pattern
1. Initial rapid improvement (generations 0-5)
2. Gradual refinement (generations 5-20)
3. Plateau phase (generations 20+)
4. Occasional breakthroughs

### Success Metrics
- Fitness > 0.9: Excellent exploration
- Fitness > 0.8: Good exploration
- Fitness > 0.7: Acceptable exploration
- Fitness < 0.5: Poor exploration

## Tips for Better Evolution

### Parameter Tuning
1. Population Size
   - Larger populations (200+) for better diversity
   - Smaller populations (50-) for faster evolution
   - Balance with computation time

2. Number of Generations
   - More generations for better solutions
   - Watch for plateauing
   - Typical range: 50-200 generations

3. Mutation Rate
   - Higher rates (0.05) for more exploration
   - Lower rates (0.01) for refinement
   - Default: 0.02

### Common Patterns in Successful Programs
1. Wall Following
   ```
   Nxxx 0 -> E 0  # Follow North wall
   xxxS 0 -> W 0  # Follow South wall
   ```

2. Corner Handling
   ```
   NExx 0 -> S 1  # Handle NE corner
   NxWx 0 -> E 1  # Handle NW corner
   ```

3. State Management
   - Using different states for different behaviors
   - State transitions for pattern recognition
   - Memory of previous positions

## Debugging Tips

### Common Issues
1. Premature Convergence
   - Increase population size
   - Adjust mutation rate
   - Add diversity mechanisms

2. Poor Exploration
   - Check fitness evaluation
   - Verify trial count
   - Review selection pressure

3. Slow Evolution
   - Reduce population size
   - Adjust selection criteria
   - Optimize evaluation process

### Performance Optimization
1. Parallel Evaluation
   - Run multiple trials simultaneously
   - Use multiprocessing
   - Batch program evaluation

2. Early Stopping
   - Monitor convergence
   - Stop when plateaued
   - Save best program

## Related Features
- Classic Mode: Compare evolved programs with random ones
- LLM Mode: Compare with AI-driven solutions
- Custom Maps: Test evolved programs in different environments
- Program Analysis: Tools for understanding evolved strategies

## Best Practices
1. Start with default parameters
2. Monitor fitness progression
3. Save successful programs
4. Experiment with parameters
5. Compare multiple runs
6. Document successful configurations 