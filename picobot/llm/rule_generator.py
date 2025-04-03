"""Rule generation using LLM providers."""

from typing import Dict, List, Tuple
from .base import LLMInterface
from ..program import Program
from ..game.state import State

def generate_rules(provider: LLMInterface) -> Program:
    """Generate a complete set of Picobot rules using an LLM provider.
    
    Args:
        provider: The LLM provider to use for rule generation
        
    Returns:
        Program object with the generated rules
    """
    # Create a prompt that explains what we need
    prompt = """You are a Picobot rule generator. Your task is to generate a complete set of rules that will allow the robot to explore its environment efficiently.

The rules must follow this EXACT format:
STATE PATTERN -> MOVE NEXT_STATE

Where:
- STATE is a number from 0 to 4
- PATTERN is a 4-character string representing walls (N, S, E, W) or no walls (x)
- MOVE is one of: N, S, E, W
- NEXT_STATE is a number from 0 to 4

PATTERN FORMAT:
- The pattern must be exactly 4 characters long
- Use N, S, E, W for walls in those directions
- Use x for no wall in that direction
- NO SPACES in the pattern
- NO WILDCARDS (*)

VALID PATTERN EXAMPLES:
xxxx (no walls)
Nxxx (wall to north)
xExx (wall to east)
xxWx (wall to west)
xxxS (wall to south)
NExx (walls to north and east)
xxWS (walls to west and south)

INVALID PATTERN EXAMPLES:
* * * * (has spaces)
N*** (uses wildcards)
N x x x (has spaces)
N*W* (uses wildcards)

Example rules:
0 xxxx -> E 0
0 Nxxx -> E 1
0 xExx -> N 0
0 xxWS -> N 1
1 xxxx -> S 1
1 NExx -> W 1
1 xxWS -> N 0

Generate a complete set of rules that:
1. Uses all 5 states (0-4)
2. Covers all possible wall patterns
3. Implements a wall-following strategy
4. Avoids getting stuck in loops
5. Uses state transitions strategically

IMPORTANT: Each rule must be on its own line and follow the exact format shown above."""

    try:
        # Create a dummy state to get rules from LLM
        dummy_state = State(
            position=(0, 0),
            walls={
                "North": False,
                "East": False,
                "South": False,
                "West": False
            },
            visited=set(),
            steps=0
        )
        
        # Get rules from LLM using the provider's interface
        response = provider.get_next_move(dummy_state)
        
        # Parse the rules from the response's reasoning field
        rules_text = response['reasoning'].strip()
        
        # Create a new program
        program = Program()
        
        # Add each rule to the program
        for line in rules_text.split('\n'):
            line = line.strip()
            if not line or '->' not in line or line.startswith('#'):
                continue
                
            try:
                # Parse rule format: "PATTERN STATE->MOVE NEWSTATE"
                pattern_state, move_newstate = line.split('->')
                pattern_state = pattern_state.strip()
                move_newstate = move_newstate.strip()
                
                # Split pattern and state
                parts = pattern_state.split()
                if len(parts) != 2:
                    print(f"Warning: Invalid pattern_state format in rule '{line}'")
                    continue
                    
                pattern, state_str = parts
                # Validate pattern format
                if len(pattern) != 4 or not all(c in 'NSEWx' for c in pattern):
                    print(f"Warning: Invalid pattern format in rule '{line}'")
                    continue
                    
                try:
                    state = int(state_str)
                except ValueError:
                    print(f"Warning: Invalid state number in rule '{line}'")
                    continue
                
                # Split move and new state
                parts = move_newstate.split()
                if len(parts) != 2:
                    print(f"Warning: Invalid move_newstate format in rule '{line}'")
                    continue
                    
                move, new_state_str = parts
                try:
                    new_state = int(new_state_str)
                except ValueError:
                    print(f"Warning: Invalid new state number in rule '{line}'")
                    continue
                
                # Validate move
                if move not in ['N', 'S', 'E', 'W']:
                    print(f"Warning: Invalid move '{move}' in rule '{line}'")
                    continue
                
                # Validate states
                if not (0 <= state <= 4 and 0 <= new_state <= 4):
                    print(f"Warning: Invalid state number in rule '{line}'")
                    continue
                
                # Add rule to program's rules_dict
                program.rules_dict[(state, pattern)] = (move, new_state)
                
            except Exception as e:
                print(f"Warning: Failed to parse rule '{line}': {str(e)}")
                continue
        
        # Verify we have all necessary rules
        from ..constants import VALID_PATTERNS, MAX_STATES
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
            for state, pattern in missing_rules:
                # Get possible moves by removing wall directions from pattern
                possible_moves = ["N", "S", "E", "W"]
                for char in pattern:
                    if char != "x":
                        possible_moves.remove(char)
                move = possible_moves[0]  # Take first valid move
                program.rules_dict[(state, pattern)] = (move, state)  # Stay in same state
        
        return program
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate rules: {str(e)}") 