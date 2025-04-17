"""Constants for the Picobot game."""

# Grid dimensions
ROWS = 20
COLUMNS = 20

# Cell states
EMPTY = False
OBSTACLE = True

# Program parameters
MAX_STATES = 5
TRIALS = 20
STEPS = 800
MUTATION_RATE = 0.02
TOP_FRACTION = 0.2

# Valid patterns for the robot's rules
VALID_PATTERNS = [
    "xxxx",  # No walls
    "Nxxx",  # Wall to the north
    "NExx",  # Walls to the north and east
    "NxWx",  # Walls to the north and west
    "xxxS",  # Wall to the south
    "xExS",  # Walls to the east and south
    "xxWS",  # Walls to the west and south
    "xExx",  # Wall to the east
    "xxWx",  # Wall to the west
]

# Visualization settings
CELL_SIZE = 30
WINDOW_WIDTH = COLUMNS * CELL_SIZE + 2 * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE + 2 * CELL_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0) 