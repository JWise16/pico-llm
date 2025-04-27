"""Wall-following prompt for Picobot rule generation."""

WALL_FOLLOWING_PROMPT = """Generate a complete set of Picobot rules that will allow the robot to explore its environment efficiently using a consistent wall-following strategy.

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
1. Implement a right-hand wall-following strategy:
   - State 0: Initial state, find a wall to follow
   - State 1: Following wall on right
   - State 2: Handling corners (turning right)
   - State 3: Recovery from stuck positions
   - State 4: Special cases and backtracking

2. State Transitions:
   - State 0 -> State 1: When wall found on right
   - State 1 -> State 2: When hitting a corner
   - State 2 -> State 1: After turning corner
   - Any State -> State 3: When stuck
   - State 3 -> State 4: When recovery needed
   - State 4 -> State 0: When back on track

3. Movement Priorities:
   - When no walls: Move until finding a wall
   - When wall on right: Follow it
   - When corner: Turn right
   - When stuck: Try alternate directions

4. Coverage Optimization:
   - Keep wall on right whenever possible
   - Turn right at corners to maintain wall contact
   - Use recovery states to escape dead ends
   - Ensure systematic coverage of the space

5. Anti-Loop Measures:
   - Use state transitions to track progress
   - Change states when stuck
   - Have clear conditions for state changes
   - Ensure forward progress

EXAMPLE RULES:
State 0 (Finding wall):
- xxxx -> E 0 (Move east until wall found)
- xExx -> S 1 (Wall found on right, start following)

State 1 (Following wall):
- xxxS -> E 1 (Wall on right, keep moving)
- xExx -> S 1 (Wall on right, keep moving)
- NExx -> S 2 (Corner found, prepare to turn)

State 2 (Turning corner):
- NExx -> S 1 (Turn right at corner)
- NxWx -> E 1 (Turn right at corner)

State 3 (Recovery):
- xxxx -> N 4 (Try moving away from stuck position)
- Nxxx -> E 4 (Try alternate direction)

State 4 (Special cases):
- xxxx -> W 0 (Return to initial state)
- xxxS -> N 0 (Return to initial state)

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 