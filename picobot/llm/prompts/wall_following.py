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
1. Use a consistent wall-following direction:
   - State 0: Follow right-hand wall (prefer moving right when possible)
   - State 1: Follow left-hand wall (prefer moving left when possible)
   - State 2: Handle corners and special cases
   - State 3: Backup state for when stuck
   - State 4: Recovery state for complex situations

2. State Transitions:
   - Stay in the same state when continuing along a wall
   - Only change states when:
     a) Hitting a corner (use state 2)
     b) Getting stuck (use state 3)
     c) Need to recover (use state 4)

3. Movement Priorities:
   - When no walls: Move in preferred direction
   - When wall ahead: Turn along the wall
   - When corner: Use special corner handling
   - When stuck: Use backup movement

4. Avoid Loops:
   - Don't keep switching between states unnecessarily
   - Use state transitions strategically
   - Have clear conditions for state changes

Respond with a JSON object containing a "rules" array, where each rule has:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)""" 