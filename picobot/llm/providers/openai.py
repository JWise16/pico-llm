import json
from typing import Dict, Any, Optional
import os
from openai import OpenAI
from httpx import Timeout
from ..base import LLMInterface, LLMResponse
from ...config.llm_config import LLMConfig
from ...game.state import State

class OpenAIProvider(LLMInterface):
    """OpenAI implementation of the LLM interface."""
    
    def __init__(self, model_name: str, temperature: float = 0.7, config: Optional[LLMConfig] = None):
        super().__init__(model_name, temperature)
        self.config = config or LLMConfig()
        
        # Initialize OpenAI client with proper configuration
        self.client = OpenAI(
            api_key=self.config.openai_api_key,
            timeout=Timeout(
                connect=2.0,    # connection timeout
                read=10.0,      # read timeout
                write=3.0,      # write timeout
                pool=5.0        # pool timeout
            ),
            max_retries=self.config.max_retries,
            default_headers={   # Add headers for better error tracking
                "X-Application": "picobot",
                "X-Application-Version": "1.0.0"
            }
        )
        
        self.model_config = self.config.openai_models.get(model_name, {})
        
        # Add chat completions interface
        self.chat = self.client.chat
    
    def initialize(self) -> None:
        """Initialize the OpenAI client."""
        if not self.config.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        
        # Test the connection with a simple request
        try:
            self.client.with_options(timeout=5.0).chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": "Test connection. Respond in JSON format."}],
                max_tokens=1,
                response_format={"type": "json_object"}
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def get_next_move(self, state: State) -> Dict[str, Any]:
        """Get the next move from OpenAI's LLM.
        
        Args:
            state: Current game state
            
        Returns:
            Dictionary containing move, reasoning, and confidence
        """
        # Format the state for the prompt
        state_desc = f"""Current Position: ({state.position[0]}, {state.position[1]})
Walls: {state.walls}
Visited Cells: {len(state.visited)}
Total Steps: {state.steps}"""
        
        try:
            # Create the message with the prompt
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Picobot controller that always responds in valid JSON format with move, reasoning, and confidence fields."
                    },
                    {
                        "role": "user",
                        "content": f"""You are controlling a Picobot in a grid-based environment. Your task is to navigate while avoiding walls and maximizing exploration.

Current State:
{state_desc}

Please analyze the state and choose the next move. Respond in JSON format with:
- move: The chosen direction (N/E/W/S)
- reasoning: Your explanation for the choice
- confidence: Your confidence in the move (0.0 to 1.0)"""
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.model_config.get("max_tokens", 1000),
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            try:
                move_data = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON response: {str(e)}")
            
            # Validate the move
            if move_data["move"] not in ["N", "E", "W", "S"]:
                raise ValueError(f"Invalid move: {move_data['move']}")
            
            # Update metrics
            self.total_tokens += response.usage.total_tokens
            self.total_cost += (response.usage.total_tokens / 1000) * self.model_config.get("cost_per_1k_tokens", 0.002)
            
            return {
                "move": move_data["move"],
                "reasoning": move_data["reasoning"],
                "confidence": move_data["confidence"]
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to get move from OpenAI: {str(e)}")
    
    def cleanup(self) -> None:
        """Clean up any resources used by the provider."""
        # OpenAI client doesn't need cleanup
        pass 