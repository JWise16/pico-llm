"""Systematic exploration prompt for Picobot rule generation."""

SYSTEMATIC_PROMPT = """Generate a complete set of Picobot rules that will allow the robot to explore its environment systematically using a grid-based approach.

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

STRATEGY REQUIREMENTS:
1. Use a systematic grid-based exploration approach:
   - State 0: Move in a consistent direction (e.g., east) until hitting a wall
   - State 1: When hitting a wall, move along it until finding an opening
   - State 2: When finding an opening, move into it and continue exploration
   - State 3: When stuck, backtrack to the last decision point
   - State 4: Handle special cases and recovery

2. State Transitions:
   - State 0 -> State 1: When hitting a wall
   - State 1 -> State 2: When finding an opening
   - State 2 -> State 0: Continue exploration in new direction
   - Any State -> State 3: When stuck or in a loop
   - State 3 -> State 4: When backtracking fails
   - State 4 -> State 0: When recovered

3. Movement Priorities:
   - When no walls: Move in the current exploration direction
   - When wall ahead: Turn along the wall
   - When opening found: Move into it
   - When stuck: Backtrack to last decision point

4. Avoid Loops:
   - Use state transitions to break out of loops
   - Implement a systematic backtracking mechanism
   - Have clear conditions for when to change exploration direction

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 