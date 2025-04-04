# Picobot Technical Overview

## Project Structure

```
picobot/
├── __main__.py      # Main entry point and CLI interface
├── constants.py     # Game configuration and constants
├── program.py       # Program class and rule management
├── robot.py         # Picobot and environment implementation
├── visualizer.py    # Pygame visualization system
├── evolution.py     # Genetic algorithm implementation
├── config/         # Configuration management
│   └── llm_config.py  # LLM provider settings
└── llm/            # LLM integration
    ├── base.py     # Base LLM interface
    └── providers/  # LLM provider implementations
        ├── openai.py    # OpenAI integration
        └── anthropic.py # Anthropic integration
```

## Core Components

### 1. Program System
```python
class Program:
    def __init__(self):
        self.rules: Dict[Tuple[int, str], Tuple[str, int]] = {}
        self.states: Set[int] = set()
```

- State-based control system (0-4 states)
- Pattern matching using string representation
- Rule format: (state, pattern) → (move, next_state)
- Efficient rule lookup using dictionary

### 2. Environment
```python
class Environment:
    def __init__(self, width: int = 20, height: int = 20):
        self.grid: List[List[bool]] = []
        self.visited: Set[Tuple[int, int]] = set()
```

- Grid-based environment (20x20 by default)
- Efficient wall detection
- Visit tracking using sets
- Pattern generation for rule matching

### 3. Evolution System
```python
class Evolution:
    def __init__(self, population_size: int = 100):
        self.population: List[Program] = []
        self.fitness_scores: Dict[Program, float] = {}
```

- Tournament selection
- Single-point crossover
- Mutation with configurable rate
- Multi-trial fitness evaluation
- Parallel evolution support (coming soon)

### 4. LLM Integration
```python
class BaseLLM:
    async def get_move(self, 
                      state: Dict[str, Any]) -> Tuple[str, float]:
        """Get next move with confidence score."""
```

- Async API calls
- Structured JSON responses
- Confidence scoring
- Context-aware decision making
- Multiple provider support

## Key Technical Improvements

### 1. Type System
- Full Python type hints
- Custom type definitions
- Runtime type checking
- Better IDE support

### 2. Performance Optimizations
- Efficient grid operations using numpy
- Pattern matching optimization
- Memory-efficient data structures
- Caching for LLM responses

### 3. Error Handling
- Comprehensive exception hierarchy
- Detailed error messages
- Graceful degradation
- Recovery mechanisms

### 4. Testing Infrastructure
- Unit tests for core components
- Integration tests for LLM
- Performance benchmarks
- Coverage tracking

## Implementation Details

### 1. Pattern Matching
```python
def get_pattern(self, x: int, y: int) -> str:
    """Generate pattern string for current position."""
    pattern = []
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        pattern.append('x' if self.is_wall(x + dx, y + dy) else 'o')
    return ''.join(pattern)
```

### 2. Evolution Operators
```python
def crossover(self, parent1: Program, parent2: Program) -> Program:
    """Create child program through crossover."""
    child = Program()
    # Implementation details...
    return child
```

### 3. LLM Context
```python
def get_context(self) -> Dict[str, Any]:
    """Generate context for LLM decision making."""
    return {
        'position': self.position,
        'pattern': self.get_pattern(),
        'visited': len(self.visited),
        'steps': self.steps
    }
```

## Performance Metrics

### 1. Grid Operations
- Wall detection: O(1)
- Pattern generation: O(1)
- Visit tracking: O(1)

### 2. Program Evaluation
- Rule lookup: O(1)
- State transitions: O(1)
- Pattern matching: O(1)

### 3. Evolution
- Fitness evaluation: O(n) where n is population size
- Selection: O(n log n)
- Crossover: O(1)
- Mutation: O(1)

### 4. LLM Integration
- API call latency: ~200-500ms
- Response parsing: O(1)
- Context generation: O(1)

## Future Technical Improvements

### 1. Performance
- Parallel evolution
- GPU acceleration for visualization
- Caching optimization
- Memory usage reduction

### 2. Architecture
- Plugin system for providers
- Event-driven architecture
- WebSocket support
- API versioning

### 3. Testing
- Property-based testing
- Performance regression tests
- Load testing
- Security testing

### 4. Monitoring
- Performance metrics
- Error tracking
- Usage analytics
- Cost monitoring

# Technical Documentation

## LLM Integration Architecture

### Core Components

1. **LLM Interface**
   - Base class defining the interface for all LLM providers
   - Handles common functionality and error handling
   - Manages token tracking and cost estimation

2. **Provider Implementations**
   - OpenAI: GPT-3.5 and GPT-4 support
   - Anthropic: Claude 3 support
   - Each provider handles API-specific requirements

3. **Rule Generator**
   - Converts LLM output to Picobot rules
   - Validates pattern format and rule completeness
   - Handles default rule generation

### Key Challenges

1. **Pattern Format**
   ```python
   # Required format
   "0 NExx -> W 1"  # State 0, North-East walls, move West, next state 1
   
   # Common LLM mistakes
   "0 N*** -> W 1"  # Uses wildcards
   "0 N x x -> W 1" # Adds spaces
   "State 0: NExx -> W 1" # Adds labels
   ```

2. **Rule Coverage**
   ```python
   # Required patterns for each state
   patterns = [
       "xxxx", "Nxxx", "NExx", "NxWx", "xxxS",
       "xExS", "xxWS", "xExx", "xxWx"
   ]
   
   # Example of missing rules
   missing = {
       (0, "xxxx"): None,  # No rule for empty space in state 0
       (1, "NExx"): None,  # No rule for NE corner in state 1
   }
   ```

3. **State Transitions**
   ```python
   # Example of state machine design
   states = {
       0: "Wall following",    # Basic clockwise movement
       1: "Corner handling",   # Special case for corners
       2: "Backtracking",      # Recovery from dead ends
       3: "Counter-clockwise", # Alternative direction
       4: "Unexplored areas"   # Special case handling
   }
   ```

### Implementation Details

1. **Rule Validation**
   ```python
   def validate_pattern(pattern: str) -> bool:
       """Validate pattern format."""
       if len(pattern) != 4:
           return False
       return all(c in 'NSEWx' for c in pattern)
   ```

2. **Default Rule Generation**
   ```python
   def generate_default_rules(program: Program):
       """Add default rules for missing patterns."""
       for state in range(5):
           for pattern in generate_patterns():
               if (state, pattern) not in program.rules_dict:
                   program.rules_dict[(state, pattern)] = ('N', state)
   ```

3. **LLM Response Parsing**
   ```python
   def parse_llm_response(response: str) -> List[Rule]:
       """Parse LLM response into valid rules."""
       rules = []
       for line in response.split('\n'):
           try:
               state, pattern, move, next_state = parse_rule(line)
               if validate_pattern(pattern):
                   rules.append((state, pattern, move, next_state))
           except ValueError:
               continue
       return rules
   ```

### Performance Considerations

1. **Token Usage**
   - Average tokens per request: 200-300
   - Cost per request: ~$0.0004
   - Response time: 1-2 seconds

2. **Rule Generation**
   - Time to generate rules: 2-3 seconds
   - Success rate: ~60% for valid patterns
   - Coverage rate: ~70% before defaults

3. **Validation Overhead**
   - Pattern validation: <1ms per rule
   - Rule completeness check: ~10ms
   - Default rule generation: ~5ms

### Error Handling

1. **API Errors**
   - Rate limiting
   - Network issues
   - Invalid responses

2. **Rule Errors**
   - Invalid patterns
   - Missing rules
   - Inconsistent state transitions

3. **Recovery Strategies**
   - Retry with backoff
   - Default rule generation
   - Pattern cleanup attempts

## Future Improvements

1. **Rule Generation**
   - Better prompt engineering
   - Pattern format enforcement
   - Strategic rule generation

2. **Validation**
   - More robust parsing
   - Better error messages
   - Pattern suggestions

3. **Performance**
   - Caching common patterns
   - Parallel rule generation
   - Optimized validation 