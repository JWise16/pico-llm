"""Module for managing prompts used by LLM providers."""

from typing import Dict, Optional

# Dictionary of available prompts
PROMPTS: Dict[str, str] = {
    'basic': """Generate a complete set of Picobot rules that will allow the robot to explore its environment efficiently.

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

IMPORTANT: You MUST generate rules for ALL of these patterns for EACH state:
- xxxx (no walls)
- Nxxx (wall to north)
- NExx (walls to north and east)
- NxWx (walls to north and west)
- xxxS (wall to south)
- xExS (walls to east and south)
- xxWS (walls to west and south)
- xExx (wall to east)
- xxWx (wall to west)

Generate a complete set of rules that:
1. Uses all 5 states (0-4)
2. Covers ALL possible wall patterns listed above for EACH state
3. Implements a wall-following strategy
4. Avoids getting stuck in loops
5. Uses state transitions strategically

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""",

    'wall_following': """Generate a set of Picobot rules that implements a wall-following strategy.

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

The wall-following strategy should:
1. Keep the wall on the right side when possible
2. Turn right when hitting a wall
3. Move forward when no wall is detected
4. Use states to remember the last move direction
5. Handle corners and dead ends gracefully

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""",

    'exploration': """Generate a set of Picobot rules that implements an exploration strategy.

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

The exploration strategy should:
1. Prioritize unexplored areas
2. Use states to remember visited locations
3. Avoid getting stuck in loops
4. Handle dead ends by backtracking
5. Use a systematic approach to cover the entire space

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)"""
}

def get_prompt(prompt_name: str = 'basic') -> str:
    """Get a prompt by name.
    
    Args:
        prompt_name: Name of the prompt to retrieve
        
    Returns:
        The requested prompt
        
    Raises:
        ValueError: If the prompt name is not found
    """
    if prompt_name not in PROMPTS:
        raise ValueError(f"Unknown prompt name: {prompt_name}")
    return PROMPTS[prompt_name]

def list_available_prompts() -> list[str]:
    """Get a list of available prompt names.
    
    Returns:
        List of available prompt names
    """
    return list(PROMPTS.keys()) 