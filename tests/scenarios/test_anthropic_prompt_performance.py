#!/usr/bin/env python3
"""Test suite for analyzing Anthropic model prompt performance in Picobot."""

import pytest
import time
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.robot import Picobot
from picobot.program import Program
from picobot.constants import ROWS, COLUMNS, VALID_PATTERNS, MAX_STATES

# Load environment variables
load_dotenv()

@pytest.fixture
def output_dir():
    """Get the output directory from environment variable."""
    return os.getenv("PICOBOT_OUTPUT_DIR", "results/anthropic_analysis")

@pytest.fixture
def anthropic_provider():
    """Create an Anthropic provider instance."""
    provider = AnthropicProvider(model_name="claude-3-opus-20240229")
    provider.initialize()
    return provider

@pytest.fixture
def test_maze():
    """Create a test maze."""
    # Create a 20x20 maze with a simple pattern
    maze = [["#" for _ in range(COLUMNS)] for _ in range(ROWS)]
    
    # Add a simple path in the middle
    for i in range(5, 15):
        for j in range(5, 15):
            maze[i][j] = " "
    
    # Convert to string format for compatibility
    return ["".join(row) for row in maze]

def create_program_from_rules(rules):
    """Create a Program instance from a list of Rule objects."""
    program = Program()
    
    # Validate that we have rules for all required patterns
    required_patterns = set(VALID_PATTERNS)
    provided_patterns = set()
    
    for rule in rules:
        # Validate rule format
        if not hasattr(rule, 'state') or not hasattr(rule, 'pattern') or \
           not hasattr(rule, 'move') or not hasattr(rule, 'next_state'):
            raise ValueError(f"Invalid rule format: {rule}")
            
        # Validate pattern
        if rule.pattern not in VALID_PATTERNS:
            raise ValueError(f"Invalid pattern in rule: {rule.pattern}")
            
        # Validate move
        if rule.move not in ["N", "E", "W", "S"]:
            raise ValueError(f"Invalid move in rule: {rule.move}")
            
        # Validate state
        if not 0 <= rule.state < MAX_STATES or not 0 <= rule.next_state < MAX_STATES:
            raise ValueError(f"Invalid state in rule: {rule.state} -> {rule.next_state}")
            
        # Add rule to program
        program.rules_dict[(rule.state, rule.pattern)] = (rule.move, rule.next_state)
        provided_patterns.add(rule.pattern)
    
    # Check if all required patterns are covered
    missing_patterns = required_patterns - provided_patterns
    if missing_patterns:
        raise ValueError(f"Missing rules for patterns: {missing_patterns}")
    
    return program

def run_simulation(anthropic_provider, prompt_name, maze, max_steps=1000):
    """Run a simulation with the given prompt and return performance metrics."""
    try:
        print(f"\nGenerating rules for {prompt_name} prompt...")
        # Get rules from Anthropic
        rules = anthropic_provider.generate_rules(prompt_name)
        print(f"Generated {len(rules)} rules")
        
        # Create program and initialize Picobot
        print("Creating program from rules...")
        program = create_program_from_rules(rules)
        
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
            
        print(f"Starting position: ({start_row}, {start_col})")
        picobot = Picobot(start_row, start_col, program)
        
        # Run simulation without visualization
        print("Running simulation...")
        steps_taken = 0
        while steps_taken < max_steps:
            if picobot.step():
                steps_taken += 1
            else:
                print(f"\nRobot appears to be stuck after {steps_taken} steps. Terminating simulation.")
                break
            
            # Check if robot is stuck (no movement for 10 steps)
            if steps_taken > 10 and picobot.is_stuck():
                print(f"\nRobot appears to be stuck after {steps_taken} steps. Terminating simulation.")
                break
        
        # Calculate coverage (only count visits to open cells)
        total_open_cells = sum(row.count(' ') for row in maze)
        visited_open_cells = 0
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == ' ' and picobot.array[i][j].visited:
                    visited_open_cells += 1
        coverage = (visited_open_cells / total_open_cells) * 100
        
        # Determine success (>80% coverage and completed within max steps)
        success = coverage > 80 and steps_taken < max_steps
        
        print(f"Simulation completed:")
        print(f"- Steps taken: {steps_taken}")
        print(f"- Coverage: {coverage:.2f}%")
        print(f"- Success: {success}")
        
        return {
            'steps': steps_taken,
            'coverage': coverage,
            'success': success
        }
        
    except Exception as e:
        print(f"Error running simulation: {str(e)}")
        return {
            'steps': max_steps,
            'coverage': 0,
            'success': False,
            'error': str(e)
        }

def test_prompt_performance(anthropic_provider, test_maze, output_dir):
    """Test performance of different prompts."""
    prompts = [
        'basic',
        'wall_following',
        'systematic',
        'english',
        'spiral',
        'snake',
        'zigzag'
    ]
    
    results = {}
    
    # Create results directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for name in prompts:
        print(f"\n{'='*50}")
        print(f"Testing {name} prompt...")
        print(f"{'='*50}")
        
        try:
            # Run simulation and get results
            result = run_simulation(anthropic_provider, name, test_maze)
            results[name] = result
            
            # Print detailed results
            print(f"\nResults for {name}:")
            print(f"- Coverage: {result['coverage']:.2f}%")
            print(f"- Steps taken: {result['steps']}")
            print(f"- Success: {result['success']}")
            
            if 'error' in result:
                print(f"- Error: {result['error']}")
            
            # Save individual prompt results
            prompt_file = Path(f'{output_dir}/{name}_results.json')
            with open(prompt_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            # Add delay to prevent rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error testing {name} prompt: {str(e)}")
            results[name] = {
                'steps': 1000,
                'coverage': 0,
                'success': False,
                'error': str(e)
            }
    
    # Analyze results
    successful_prompts = [name for name, result in results.items() if result['success']]
    print("\nAnalysis Summary:")
    print(f"Total prompts tested: {len(prompts)}")
    print(f"Successful prompts: {len(successful_prompts)}")
    
    # Sort prompts by coverage
    sorted_results = sorted(
        results.items(),
        key=lambda x: (x[1]['coverage'], -x[1]['steps']),
        reverse=True
    )
    
    print("\nPrompt Rankings (by coverage):")
    for name, result in sorted_results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {name:12} - Coverage: {result['coverage']:5.1f}% in {result['steps']:4d} steps")
    
    # Save detailed results
    with open(f'{output_dir}/summary.txt', 'w') as f:
        f.write("ANTHROPIC PROMPT PERFORMANCE ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Overview:\n")
        f.write(f"- Total prompts tested: {len(prompts)}\n")
        f.write(f"- Successful prompts: {len(successful_prompts)}\n")
        f.write(f"- Success rate: {len(successful_prompts)/len(prompts)*100:.1f}%\n\n")
        
        f.write("Detailed Results:\n")
        for name, result in sorted_results:
            f.write(f"\n{name.upper()}\n")
            f.write("-" * len(name) + "\n")
            f.write(f"Coverage: {result['coverage']:.2f}%\n")
            f.write(f"Steps: {result['steps']}\n")
            f.write(f"Success: {result['success']}\n")
            if 'error' in result:
                f.write(f"Error: {result['error']}\n")
    
    # Assert that at least one prompt was successful
    assert len(successful_prompts) > 0, f"No prompts achieved successful performance. Best coverage was {sorted_results[0][1]['coverage']:.1f}% by {sorted_results[0][0]}" 