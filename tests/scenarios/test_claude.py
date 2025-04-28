import pytest
import os
from dotenv import load_dotenv
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.llm.base import LLMInterface
from picobot.game.environment import Environment
from picobot.robot import Picobot
from picobot.program import Program
import random
import json
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def anthropic_provider():
    return AnthropicProvider()

@pytest.fixture
def environment():
    return Environment(width=5, height=5)

@pytest.fixture
def test_maze():
    """Create a test maze."""
    # Create a 20x20 maze with a simple pattern
    maze = [["#" for _ in range(20)] for _ in range(20)]
    
    # Add a simple path in the middle
    for i in range(5, 15):
        for j in range(5, 15):
            maze[i][j] = " "
    
    # Convert to string format for compatibility
    return ["".join(row) for row in maze]

def create_program_from_rules(rules):
    """Create a Program instance from a list of Rule objects."""
    program = Program()
    
    # Add rules to program
    for rule in rules:
        program.rules_dict[(rule.state, rule.pattern)] = (rule.move, rule.next_state)
    
    return program

def run_simulation(program, maze, max_steps=1000):
    """Run a simulation with the given program and return performance metrics."""
    # Find a valid starting position (not a wall)
    start_row = None
    start_col = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == ' ':
                start_row = i
                start_col = j
                break
        if start_row is not None:
            break
            
    if start_row is None:
        raise ValueError("No valid starting position found in maze")
        
    # Initialize Picobot
    picobot = Picobot(start_row, start_col, program)
    
    # Run simulation
    steps_taken = 0
    while steps_taken < max_steps:
        if picobot.step():
            steps_taken += 1
        else:
            break
        
        # Check if robot is stuck
        if steps_taken > 10 and picobot.is_stuck():
            break
    
    # Calculate coverage
    total_open_cells = sum(row.count(' ') for row in maze)
    visited_open_cells = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == ' ' and picobot.array[i][j].visited:
                visited_open_cells += 1
    coverage = (visited_open_cells / total_open_cells) * 100
    
    return {
        'steps': steps_taken,
        'coverage': coverage,
        'success': coverage > 80 and steps_taken < max_steps
    }

def test_anthropic_initialization(anthropic_provider):
    """Test that AnthropicProvider initializes correctly"""
    assert isinstance(anthropic_provider, LLMInterface)
    assert anthropic_provider.model_name == "claude-3-opus-20240229"
    assert anthropic_provider.temperature == 0.7

def test_rule_generation(anthropic_provider):
    """Test that AnthropicProvider can generate valid rules"""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    
    # Initialize the provider with API key
    anthropic_provider.initialize(api_key=api_key)
    
    try:
        # Generate rules
        rules = anthropic_provider.generate_rules(prompt_name='basic', num_rules=9)
        
        # Validate rules
        assert len(rules) > 0
        for rule in rules:
            assert hasattr(rule, 'state')
            assert hasattr(rule, 'pattern')
            assert hasattr(rule, 'move')
            assert hasattr(rule, 'next_state')
            
            # Validate pattern format
            assert len(rule.pattern) == 4
            assert all(c in 'NSEWx' for c in rule.pattern)
            
            # Validate move
            assert rule.move in ['N', 'S', 'E', 'W']
            
            # Validate state transitions
            assert isinstance(rule.state, int)
            assert isinstance(rule.next_state, int)
            assert 0 <= rule.state <= 9
            assert 0 <= rule.next_state <= 9
        
        # Get usage metrics
        metrics = anthropic_provider.get_usage_metrics()
        assert metrics['total_tokens'] > 0
        assert metrics['cost'] >= 0
        
    finally:
        # Cleanup
        anthropic_provider.cleanup()

def test_wall_following_rules(anthropic_provider):
    """Test that wall-following strategy generates appropriate rules"""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    
    # Initialize the provider with API key
    anthropic_provider.initialize(api_key=api_key)
    
    try:
        # Generate rules with wall-following strategy
        rules = anthropic_provider.generate_rules(prompt_name='wall_following', num_rules=9)
        
        # Basic validation
        assert len(rules) > 0
        
        # Check for wall-following patterns
        wall_patterns = set()
        for rule in rules:
            # Add patterns that involve walls
            if any(c in 'NSEW' for c in rule.pattern):
                wall_patterns.add(rule.pattern)
        
        # Should have some patterns that deal with walls
        assert len(wall_patterns) > 0, "No wall-following patterns found"
        
        # Get usage metrics
        metrics = anthropic_provider.get_usage_metrics()
        assert metrics['total_tokens'] > 0
        assert metrics['cost'] >= 0
        
    finally:
        # Cleanup
        anthropic_provider.cleanup()

def test_all_prompts(anthropic_provider, test_maze):
    """Test all available prompts"""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    
    # Initialize the provider with API key
    anthropic_provider.initialize(api_key=api_key)
    
    # List of all prompts to test
    prompts = [
        'basic',
        'wall_following',
        'systematic',
        'english',
        'spiral',
        'snake',
        'zigzag'
    ]
    
    # Create results directory
    output_dir = Path("results/claude_tests")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    try:
        for prompt_name in prompts:
            print(f"\nTesting prompt: {prompt_name}")
            
            # Generate rules
            rules = anthropic_provider.generate_rules(prompt_name=prompt_name, num_rules=9)
            
            # Basic validation
            assert len(rules) > 0, f"No rules generated for {prompt_name}"
            
            # Validate each rule
            for rule in rules:
                assert hasattr(rule, 'state')
                assert hasattr(rule, 'pattern')
                assert hasattr(rule, 'move')
                assert hasattr(rule, 'next_state')
                
                # Validate pattern format
                assert len(rule.pattern) == 4
                assert all(c in 'NSEWx' for c in rule.pattern)
                
                # Validate move
                assert rule.move in ['N', 'S', 'E', 'W']
                
                # Validate state transitions
                assert isinstance(rule.state, int)
                assert isinstance(rule.next_state, int)
                assert 0 <= rule.state <= 9
                assert 0 <= rule.next_state <= 9
            
            # Create program and run simulation
            program = create_program_from_rules(rules)
            simulation_results = run_simulation(program, test_maze)
            
            # Get usage metrics
            metrics = anthropic_provider.get_usage_metrics()
            
            # Save results
            results[prompt_name] = {
                'num_rules': len(rules),
                'total_tokens': metrics['total_tokens'],
                'cost': metrics['cost'],
                'steps': simulation_results['steps'],
                'coverage': simulation_results['coverage'],
                'success': simulation_results['success']
            }
            
            # Save individual prompt results
            prompt_file = output_dir / f"{prompt_name}_results.json"
            with open(prompt_file, 'w') as f:
                json.dump(results[prompt_name], f, indent=2)
            
            # Add delay to prevent rate limiting
            import time
            time.sleep(2)
        
        # Save overall results
        with open(output_dir / "summary.txt", 'w') as f:
            f.write("CLAUDE PROMPT TEST RESULTS\n")
            f.write("=" * 50 + "\n\n")
            
            for prompt_name, result in results.items():
                f.write(f"{prompt_name.upper()}\n")
                f.write("-" * len(prompt_name) + "\n")
                f.write(f"Number of rules: {result['num_rules']}\n")
                f.write(f"Total tokens: {result['total_tokens']}\n")
                f.write(f"Cost: ${result['cost']:.4f}\n")
                f.write(f"Steps taken: {result['steps']}\n")
                f.write(f"Coverage: {result['coverage']:.2f}%\n")
                f.write(f"Success: {result['success']}\n\n")
        
    finally:
        # Cleanup
        anthropic_provider.cleanup() 