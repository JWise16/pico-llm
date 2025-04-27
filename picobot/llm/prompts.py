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

    'wall_following': """Generate a complete set of Picobot rules that implements a wall-following strategy.

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

WALL FOLLOWING STRATEGY:
1. State 0: Follow right wall (move clockwise)
   - If no wall on right, turn right and move
   - If wall on right, move forward
   - If blocked, turn left
2. State 1: Follow left wall (move counter-clockwise)
   - If no wall on left, turn left and move
   - If wall on left, move forward
   - If blocked, turn right
3. State 2: Handle dead ends
   - Turn around and switch wall following direction
4. State 3: Handle corridors
   - Continue in current direction if possible
   - Switch to appropriate wall following state if blocked
5. State 4: Handle intersections
   - Prefer continuing wall follow
   - Switch states if better direction available

EXAMPLE RULES:
0 xxxx -> E 0 (No walls, move east to find wall)
0 xExx -> S 1 (Wall on right, move forward)
1 xxxx -> W 1 (No walls, move west to find wall)
1 xxWx -> S 1 (Wall on left, move forward)
2 NExx -> S 1 (Turn around, switch to left wall)

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