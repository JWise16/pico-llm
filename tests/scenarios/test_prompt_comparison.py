"""Test comparison of different prompts with Claude."""

import os
from dotenv import load_dotenv
import pytest
import json
from pathlib import Path
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.robot import Picobot
from picobot.program import Program
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

@pytest.fixture
def output_dir():
    """Get the output directory from environment variable."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.getenv("PICOBOT_OUTPUT_DIR", "results/claude_comparison")
    return f"{base_dir}_{timestamp}"

@pytest.fixture
def anthropic_provider():
    """Create an AnthropicProvider instance for testing."""
    model_name = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
    provider = AnthropicProvider(
        model_name=model_name,
        temperature=0.7
    )
    provider.initialize()
    return provider

@pytest.fixture
def blank_board():
    """Create a blank 20x20 board."""
    return [[" " for _ in range(20)] for _ in range(20)]

def create_program_from_rules(rules):
    """Create a Program instance from a list of rules."""
    program = Program()
    for rule in rules:
        program.rules_dict[(rule.state, rule.pattern)] = (rule.move, rule.next_state)
    return program

def run_simulation(program, board, max_steps=1000):
    """Run a simulation with the given program and return performance metrics."""
    # Start from the center of the board
    start_row = 10
    start_col = 10
    
    print(f"\nStarting simulation at ({start_row}, {start_col})")
    
    # Initialize Picobot
    picobot = Picobot(start_row, start_col, program)
    
    # Run simulation
    steps_taken = 0
    while steps_taken < max_steps:
        if picobot.step():
            steps_taken += 1
            if steps_taken % 100 == 0:
                print(f"Step {steps_taken}: Position ({picobot.robot_row}, {picobot.robot_col}), Visited: {picobot.num_visited}")
        else:
            print(f"Invalid move at step {steps_taken}")
            break
        
        # Check if robot is stuck
        if steps_taken > 10 and picobot.is_stuck():
            print(f"Robot stuck at step {steps_taken}")
            break
    
    # Calculate coverage
    total_cells = len(board) * len(board[0])  # 20x20 = 400 cells
    coverage = (picobot.num_visited / total_cells) * 100
    
    print(f"\nSimulation completed:")
    print(f"- Total steps: {steps_taken}")
    print(f"- Cells visited: {picobot.num_visited}")
    print(f"- Coverage: {coverage:.2f}%")
    
    return {
        'steps': steps_taken,
        'coverage': coverage,
        'success': coverage > 80 and steps_taken < max_steps,
        'cells_visited': picobot.num_visited,
        'total_cells': total_cells
    }

def test_prompt_performance(anthropic_provider, blank_board, output_dir):
    """Test performance of different prompts on a blank board."""
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
    
    # Create trial metadata
    trial_data = {
        'model': anthropic_provider.model_name,
        'timestamp': datetime.now().isoformat(),
        'prompts': {}
    }
    
    for name in prompts:
        print(f"\n{'='*50}")
        print(f"Testing {name} prompt...")
        print(f"{'='*50}")
        
        try:
            # Generate rules
            print(f"Generating rules for {name} prompt...")
            rules = anthropic_provider.generate_rules(name)
            print(f"Generated {len(rules)} rules")
            
            # Create program
            program = create_program_from_rules(rules)
            
            # Run simulation
            print("Running simulation...")
            result = run_simulation(program, blank_board)
            
            # Add rule count to results
            result['rules'] = len(rules)
            
            # Save results
            results[name] = result
            trial_data['prompts'][name] = result
            
            # Print detailed results
            print(f"\nResults for {name}:")
            print(f"- Coverage: {result['coverage']:.2f}%")
            print(f"- Steps taken: {result['steps']}")
            print(f"- Success: {result['success']}")
            
            # Save individual prompt results
            prompt_file = Path(f'{output_dir}/{name}_results.json')
            with open(prompt_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            # Add delay to prevent rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error testing {name} prompt: {str(e)}")
            error_result = {
                'steps': 1000,
                'coverage': 0,
                'success': False,
                'rules': 0,
                'error': str(e),
                'cells_visited': 0,
                'total_cells': 400
            }
            results[name] = error_result
            trial_data['prompts'][name] = error_result
    
    # Save trial data
    with open(f'{output_dir}/trial_data.json', 'w') as f:
        json.dump(trial_data, f, indent=2)
    
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
        f.write("CLAUDE PROMPT PERFORMANCE ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Overview:\n")
        f.write(f"- Model: {anthropic_provider.model_name}\n")
        f.write(f"- Timestamp: {datetime.now().isoformat()}\n")
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