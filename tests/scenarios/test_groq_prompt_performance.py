#!/usr/bin/env python3
"""Test suite for analyzing Groq model prompt performance in Picobot."""

import pytest
import time
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from picobot.llm.providers.groq import GroqProvider
from picobot.robot import Picobot
from picobot.program import Program
from picobot.constants import ROWS, COLUMNS, VALID_PATTERNS, MAX_STATES

# Load environment variables
load_dotenv()

@pytest.fixture
def output_dir():
    """Get the output directory."""
    # Use PICOBOT_OUTPUT_DIR if set, otherwise create a default directory
    output_dir = os.getenv("PICOBOT_OUTPUT_DIR")
    if not output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        output_dir = f"results/groq_analysis_{timestamp}/{model_name}/run_1_{timestamp}"
    return output_dir

@pytest.fixture
def groq_provider():
    """Create a Groq provider instance."""
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Use environment variable with fallback
    print(f"\nInitializing Groq provider with model: {model_name}")
    provider = GroqProvider(model_name=model_name)
    try:
        provider.initialize()  # This will use GROQ_API_KEY from .env
        print("Provider initialized successfully")
    except Exception as e:
        print(f"Error initializing provider: {str(e)}")
        raise
    return provider

def test_prompt_performance(groq_provider, output_dir):
    """Test the performance of different prompts with Groq models."""
    print("\nStarting prompt performance test")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_path}")
    
    # List of prompts to test
    prompts = ['basic', 'english', 'snake', 'spiral', 'systematic', 'wall_following', 'zigzag']
    
    results = {}
    trial_data = {
        'model': os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'prompts': {}
    }
    
    for prompt in prompts:
        print(f"\nTesting prompt: {prompt}")
        start_time = time.time()
        
        try:
            print("Generating rules...")
            rules = groq_provider.generate_rules(prompt_name=prompt, num_rules=9)
            print(f"Generated {len(rules)} rules")
            
            print("Creating program...")
            program = Program()
            for rule in rules:
                # Add rule to the program's rules dictionary
                program.rules_dict[(rule.state, rule.pattern)] = (rule.move, rule.next_state)
            
            print("Creating Picobot instance...")
            start_row = ROWS // 2
            start_col = COLUMNS // 2
            picobot = Picobot(start_row=start_row, start_col=start_col, program=program)
            
            print("Running simulation...")
            num_steps = picobot.run(steps=200)
            print(f"Simulation completed in {num_steps} steps")
            
            print("Getting metrics...")
            metrics = groq_provider.get_usage_metrics()
            
            print("Calculating visited cells...")
            visited_cells = []
            for row in range(ROWS):
                for col in range(COLUMNS):
                    if picobot.array[row][col].visited:
                        visited_cells.append((row, col))
            
            # Calculate performance metrics
            coverage = len(visited_cells) / (ROWS * COLUMNS)
            efficiency = coverage / num_steps if num_steps > 0 else 0
            
            # Store results
            prompt_results = {
                'coverage': coverage,
                'efficiency': efficiency,
                'steps': num_steps,
                'tokens': metrics['total_tokens'],
                'cost': metrics['cost'],
                'time': time.time() - start_time,
                'visited': visited_cells
            }
            
            # Save individual prompt results
            with open(output_path / f'{prompt}_results.json', 'w') as f:
                json.dump(prompt_results, f, indent=2)
            
            # Store in trial data
            trial_data['prompts'][prompt] = {
                'rules': [rule.__dict__ for rule in rules],
                'metrics': metrics,
                'performance': prompt_results
            }
            
            # Store in results for summary
            results[prompt] = prompt_results
                
        except Exception as e:
            print(f"Error testing prompt {prompt}: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            results[prompt] = {'error': str(e)}
            trial_data['prompts'][prompt] = {'error': str(e)}
    
    # Save trial data
    with open(output_path / 'trial_data.json', 'w') as f:
        json.dump(trial_data, f, indent=2)
    
    # Save summary
    with open(output_path / 'summary.txt', 'w') as f:
        f.write("Test Summary:\n")
        f.write("============\n\n")
        for prompt, result in results.items():
            if 'error' in result:
                f.write(f"{prompt}:\n")
                f.write(f"  Error: {result['error']}\n\n")
            else:
                f.write(f"{prompt}:\n")
                f.write(f"  Coverage: {result['coverage']:.2%}\n")
                f.write(f"  Efficiency: {result['efficiency']:.4f}\n")
                f.write(f"  Steps: {result['steps']}\n")
                f.write(f"  Tokens: {result['tokens']}\n")
                f.write(f"  Cost: ${result['cost']:.4f}\n")
                f.write(f"  Time: {result['time']:.2f}s\n\n")
    
    # Print summary to console
    print("\nTest Summary:")
    for prompt, result in results.items():
        if 'error' in result:
            print(f"{prompt}: Error - {result['error']}")
        else:
            print(f"{prompt}:")
            print(f"  Coverage: {result['coverage']:.2%}")
            print(f"  Efficiency: {result['efficiency']:.4f}")
            print(f"  Steps: {result['steps']}")
            print(f"  Tokens: {result['tokens']}")
            print(f"  Cost: ${result['cost']:.4f}")
            print(f"  Time: {result['time']:.2f}s")
    
    # Ensure we have at least one successful result
    successful_results = [r for r in results.values() if 'error' not in r]
    assert len(successful_results) > 0, "No prompts completed successfully" 