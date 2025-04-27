"""Zigzag pattern exploration prompt for Picobot rule generation."""

ZIGZAG_PROMPT = """Generate a complete set of Picobot rules that will allow the robot to explore its environment using an efficient zigzag pattern strategy.

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
1. Implement a zigzag pattern exploration:
   - State 0: Move diagonally up-right
   - State 1: Move diagonally down-right
   - State 2: Handle wall encounters
   - State 3: Recover from stuck positions
   - State 4: Optimize coverage in complex areas

2. State Transitions:
   - State 0 -> State 1: When hitting top or right wall
   - State 1 -> State 0: When hitting bottom or right wall
   - Any State -> State 2: When encountering unexpected wall
   - State 2 -> State 3: When stuck
   - State 3 -> State 4: When recovery needed
   - State 4 -> State 0: Resume zigzag pattern

3. Movement Priorities:
   - When no walls: Continue current diagonal direction
   - When wall ahead: Change diagonal direction
   - When corner: Use special corner handling
   - When stuck: Use recovery strategy

4. Coverage Optimization:
   - Ensure complete diagonal coverage
   - Handle both up-right and down-right diagonals
   - Manage wall encounters efficiently
   - Cover all areas systematically

5. Anti-Loop Measures:
   - Use state transitions to track diagonal progress
   - Implement systematic direction changes
   - Handle wall encounters gracefully
   - Ensure forward progress in exploration

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 