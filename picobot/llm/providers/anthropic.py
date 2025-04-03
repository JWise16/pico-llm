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
        self.total_tokens = 0
        self.total_cost = 0.0
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Anthropic client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        
        try:
            # Initialize with just the API key
            self.client = anthropic.Anthropic(api_key=api_key)
            # Test the connection with a simple request
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
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
                system="You are a Picobot controller that always responds in valid JSON format with move, reasoning, and confidence fields. When generating rules, create a sophisticated state machine that uses different states for different exploration strategies.",
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are controlling a Picobot in a grid-based environment. Your task is to navigate while avoiding walls and maximizing exploration.

Current State:
{state_desc}

Please analyze the state and choose the next move. Respond in JSON format with:
- move: The chosen direction (North/South/East/West)
- reasoning: Your explanation for the choice
- confidence: Your confidence in the move (0.0 to 1.0)

If you see a prompt about generating rules, please provide a complete set of rules in your reasoning field. The rules should use states strategically:
- State 0: Basic wall following (clockwise)
- State 1: Corner handling and direction changes
- State 2: Backtracking from dead ends
- State 3: Counter-clockwise wall following
- State 4: Special case handling for unexplored areas

Make sure to include state transitions that create an effective exploration pattern."""
                    }
                ]
            )
            
            # Update token usage
            self.total_tokens += message.usage.input_tokens + message.usage.output_tokens
            
            # Parse the response - content is now a list of content blocks
            response_text = ""
            for content_block in message.content:
                if hasattr(content_block, 'text'):
                    response_text += content_block.text
                else:
                    response_text += str(content_block)
            
            # Clean up the response text
            response_text = response_text.replace('\r', '').replace('\t', ' ')
            
            # Find the JSON part of the response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                response_text = response_text[start:end]
            
            import json
            try:
                response = json.loads(response_text)
            except json.JSONDecodeError as e:
                # Try to clean up the response text further
                response_text = ''.join(c for c in response_text if c.isprintable())
                try:
                    response = json.loads(response_text)
                except json.JSONDecodeError as e2:
                    raise ValueError(f"Failed to parse JSON response: {str(e2)}")
            
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
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get usage metrics for the provider.
        
        Returns:
            Dictionary containing usage metrics
        """
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost
        } 