"""Picobot LLM prompts module."""

from .basic import BASIC_PROMPT
from .wall_following import WALL_FOLLOWING_PROMPT
from .systematic import SYSTEMATIC_PROMPT
from .english import ENGLISH_PROMPT
from .spiral import SPIRAL_PROMPT
from .snake import SNAKE_PROMPT
from .zigzag import ZIGZAG_PROMPT

# Dictionary mapping prompt names to their content
AVAILABLE_PROMPTS = {
    'basic': BASIC_PROMPT,
    'wall_following': WALL_FOLLOWING_PROMPT,
    'systematic': SYSTEMATIC_PROMPT,
    'english': ENGLISH_PROMPT,
    'spiral': SPIRAL_PROMPT,
    'snake': SNAKE_PROMPT,
    'zigzag': ZIGZAG_PROMPT
}

def get_prompt(prompt_name: str) -> str:
    """Get a prompt by name.
    
    Args:
        prompt_name: Name of the prompt to retrieve
        
    Returns:
        The prompt content as a string
        
    Raises:
        ValueError: If the prompt name is not found
    """
    if prompt_name not in AVAILABLE_PROMPTS:
        raise ValueError(f"Unknown prompt: {prompt_name}. Available prompts: {list(AVAILABLE_PROMPTS.keys())}")
    return AVAILABLE_PROMPTS[prompt_name]

__all__ = [
    'BASIC_PROMPT',
    'WALL_FOLLOWING_PROMPT',
    'SYSTEMATIC_PROMPT',
    'ENGLISH_PROMPT',
    'SPIRAL_PROMPT',
    'SNAKE_PROMPT',
    'ZIGZAG_PROMPT'
] 