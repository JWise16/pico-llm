"""Snake pattern exploration prompt for Picobot rule generation."""

SNAKE_PROMPT = """Generate a complete set of Picobot rules that will allow the robot to explore its environment using an efficient snake pattern strategy.

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
1. Implement a snake pattern exploration:
   - State 0: Move right along current row
   - State 1: Move left along current row
   - State 2: Move down to next row
   - State 3: Handle wall encounters
   - State 4: Recover from stuck positions

2. State Transitions:
   - State 0 -> State 1: When hitting right wall
   - State 1 -> State 2: When hitting left wall
   - State 2 -> State 0: Start new row
   - Any State -> State 3: When encountering unexpected wall
   - State 3 -> State 4: When stuck
   - State 4 -> State 0: Resume snake pattern

3. Movement Priorities:
   - When no walls: Continue current row direction
   - When wall ahead: Move to next row
   - When at row end: Change direction
   - When stuck: Use recovery strategy

4. Coverage Optimization:
   - Ensure complete row coverage
   - Handle both left-to-right and right-to-left rows
   - Manage row transitions efficiently
   - Cover all areas systematically

5. Anti-Loop Measures:
   - Use state transitions to track row progress
   - Implement systematic row changes
   - Handle wall encounters gracefully
   - Ensure forward progress in exploration

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 