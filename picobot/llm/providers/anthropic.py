import os
from typing import Dict, Any
import anthropic
from ..base import LLMInterface
from ...game.state import State

class AnthropicProvider(LLMInterface):
    """Implementation of LLMInterface using Anthropic's Claude model."""
    
    def __init__(
        self,
        model: str = "claude-3-7-sonnet-20250219",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """Initialize the Anthropic provider.
        
        Args:
            model: The Claude model to use
            temperature: Temperature for response generation (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Anthropic client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        
        try:
            # Initialize with just the API key, no additional parameters
            self.client = anthropic.Client(api_key=api_key)
            # Test the connection with a simple request
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                temperature=self.temperature,
                messages=[{
                    "role": "user",
                    "content": "Test connection. Respond in JSON format."
                }]
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Anthropic client: {str(e)}")
    
    def _format_state(self, state: State) -> str:
        """Format the game state for the prompt.
        
        Args:
            state: Current game state
            
        Returns:
            Formatted state description
        """
        # Get the current position and surroundings
        x, y = state.position
        surroundings = state.get_surroundings()
        
        # Format the state description
        state_desc = f"""
Current Position: ({x}, {y})
Surroundings:
- North: {'Wall' if surroundings['North'] else 'Empty'}
- South: {'Wall' if surroundings['South'] else 'Empty'}
- East: {'Wall' if surroundings['East'] else 'Empty'}
- West: {'Wall' if surroundings['West'] else 'Empty'}
"""
        return state_desc
    
    def get_next_move(self, state: State) -> Dict[str, Any]:
        """Get the next move from the LLM.
        
        Args:
            state: Current game state
            
        Returns:
            Dictionary containing move, reasoning, and confidence
        """
        if not self.client:
            self.initialize()
        
        # Format the state and create the prompt
        state_desc = self._format_state(state)
        
        try:
            # Create the message with the prompt
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are a Picobot controller that always responds in valid JSON format with move, reasoning, and confidence fields.",
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are controlling a Picobot in a grid-based environment. Your task is to navigate while avoiding walls and maximizing exploration.

Current State:
{state_desc}

Please analyze the state and choose the next move. Respond in JSON format with:
- move: The chosen direction (North/South/East/West)
- reasoning: Your explanation for the choice
- confidence: Your confidence in the move (0.0 to 1.0)"""
                    }
                ]
            )
            
            # Parse the response - content is now a list of TextBlock objects
            response_text = message.content[0].text
            # Remove code block markers if present
            if response_text.startswith('```json\n'):
                response_text = response_text[8:]  # Remove ```json\n
            if response_text.endswith('\n```'):
                response_text = response_text[:-4]  # Remove \n```
            
            import json
            try:
                response = json.loads(response_text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON response: {str(e)}")
            
            # Validate the response
            if not all(k in response for k in ["move", "reasoning", "confidence"]):
                raise ValueError("Response missing required fields")
            
            if response["move"] not in ["North", "South", "East", "West"]:
                raise ValueError(f"Invalid move: {response['move']}")
            
            if not 0 <= response["confidence"] <= 1:
                raise ValueError(f"Invalid confidence value: {response['confidence']}")
            
            return response
            
        except Exception as e:
            raise RuntimeError(f"Failed to get next move: {str(e)}")
    
    def cleanup(self) -> None:
        """Clean up any resources used by the provider."""
        self.client = None 