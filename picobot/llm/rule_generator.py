"""Rule generation using LLM providers."""

from typing import Dict, List, Tuple, Any
from .base import LLMInterface, Rule
from ..program import Program
from ..constants import VALID_PATTERNS, MAX_STATES
from .scoring import ScoreCalculator
import json

def generate_rules(provider: LLMInterface, prompt_name: str = 'basic', evaluate: bool = True) -> Tuple[Program, Dict[str, Any]]:
    """Generate a complete set of Picobot rules using an LLM provider.
    
    Args:
        provider: The LLM provider to use for rule generation
        prompt_name: Name of the prompt to use (default: 'basic')
        evaluate: Whether to evaluate the generated program (default: True)
        
    Returns:
        Tuple of (Program object with the generated rules, evaluation results if evaluate=True)
    """
    try:
        # Get rules from LLM
        print("\nRequesting rules from LLM...")
        rules = provider.generate_rules(prompt_name=prompt_name)
        
        # Log the raw rules
        print("\nRaw rules received from LLM:")
        for rule in rules:
            print(f"  {rule}")
        
        # Check if we got any rules
        if not rules:
            print("\nWarning: No valid rules were generated by the LLM.")
            print("Will proceed with default rules only.")
        
        # Create a new program
        program = Program()
        
        # Add each rule to the program
        print("\nParsing and validating rules...")
        for rule in rules:
            # Log the rule being processed
            print(f"\nProcessing rule: {rule}")
            
            # Validate pattern format
            if len(rule.pattern) != 4:
                print(f"  Warning: Invalid pattern length in rule: {rule}")
                print(f"  Expected 4 characters, got {len(rule.pattern)}")
                continue
                
            if not all(c in 'NSEWx' for c in rule.pattern):
                print(f"  Warning: Invalid characters in pattern: {rule.pattern}")
                print(f"  Invalid characters: {[c for c in rule.pattern if c not in 'NSEWx']}")
                continue
                
            # Validate states
            if not (0 <= rule.state <= 4):
                print(f"  Warning: Invalid current state in rule: {rule}")
                print(f"  State must be between 0 and 4, got {rule.state}")
                continue
                
            if not (0 <= rule.next_state <= 4):
                print(f"  Warning: Invalid next state in rule: {rule}")
                print(f"  Next state must be between 0 and 4, got {rule.next_state}")
                continue
            
            # Validate move
            if rule.move not in ['N', 'S', 'E', 'W']:
                print(f"  Warning: Invalid move '{rule.move}' in rule: {rule}")
                print(f"  Move must be one of: N, S, E, W")
                continue
            
            # Add rule to program's rules_dict
            program.rules_dict[(rule.state, rule.pattern)] = (rule.move, rule.next_state)
            print(f"  Successfully added rule: {rule.state} {rule.pattern} -> {rule.move} {rule.next_state}")
        
        # Verify we have all necessary rules
        missing_rules = []
        for state in range(MAX_STATES):
            for pattern in VALID_PATTERNS:
                if (state, pattern) not in program.rules_dict:
                    missing_rules.append((state, pattern))
        
        if missing_rules:
            print("\nWarning: Missing rules for the following state-pattern combinations:")
            for state, pattern in missing_rules:
                print(f"  State {state}, Pattern '{pattern}'")
            
            # Add default rules for missing combinations
            print("\nAdding default rules for missing combinations...")
            for state, pattern in missing_rules:
                # Get possible moves by removing wall directions from pattern
                possible_moves = ["N", "S", "E", "W"]
                for char in pattern:
                    if char != "x":
                        possible_moves.remove(char)
                move = possible_moves[0]  # Take first valid move
                program.rules_dict[(state, pattern)] = (move, state)  # Stay in same state
                print(f"  Added default rule: {state} {pattern} -> {move} {state}")
        
        print("\nFinal rule set:")
        for (state, pattern), (move, next_state) in sorted(program.rules_dict.items()):
            print(f"  {state} {pattern} -> {move} {next_state}")
        
        # Evaluate the program if requested
        evaluation_results = {}
        if evaluate:
            print("\nEvaluating program performance...")
            calculator = ScoreCalculator(trials=3, steps_per_trial=200)
            scores = calculator.evaluate_program(program)
            evaluation_results = {
                "scores": scores,
                "explanation": calculator.get_score_explanation(scores)
            }
            print("\nEvaluation results:")
            print(evaluation_results["explanation"])
        
        return program, evaluation_results
        
    except Exception as e:
        print(f"\nError during rule generation: {str(e)}")
        raise RuntimeError(f"Failed to generate rules: {str(e)}") 