"""Spiral exploration prompt for Picobot rule generation."""

SPIRAL_PROMPT = """Generate a complete set of Picobot rules that will allow the robot to explore its environment using an efficient spiral pattern strategy.

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
1. Implement a spiral exploration pattern:
   - State 0: Move in a clockwise spiral (right, down, left, up)
   - State 1: Handle wall encounters and adjust spiral direction
   - State 2: Manage corner cases and spiral expansion
   - State 3: Recover from stuck positions
   - State 4: Optimize coverage in complex areas

2. State Transitions:
   - State 0 -> State 1: When encountering a wall
   - State 1 -> State 2: When at a corner
   - State 2 -> State 0: Continue spiral pattern
   - Any State -> State 3: When stuck
   - State 3 -> State 4: When recovery needed
   - State 4 -> State 0: Resume spiral pattern

3. Movement Priorities:
   - When no walls: Follow spiral pattern (right, down, left, up)
   - When wall ahead: Turn along wall and continue spiral
   - When corner: Adjust spiral direction
   - When stuck: Use recovery strategy

4. Coverage Optimization:
   - Use state transitions to ensure complete coverage
   - Implement a systematic spiral expansion
   - Handle both clockwise and counter-clockwise turns
   - Ensure no areas are missed

5. Anti-Loop Measures:
   - Track visited areas using state transitions
   - Implement spiral expansion to cover new areas
   - Use recovery states to break out of loops
   - Ensure forward progress in exploration

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 