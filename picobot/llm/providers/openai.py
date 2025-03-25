import json
from typing import Dict, Any, Optional
import os
from openai import OpenAI
from httpx import Timeout
from ..base import LLMInterface, LLMResponse
from ...config.llm_config import LLMConfig

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
    
    def cleanup(self) -> None:
        """Clean up OpenAI resources."""
        pass
    
    def _format_state(self, current_state: Dict[str, Any], history: Optional[list] = None) -> str:
        """Format the current game state into a prompt-friendly string."""
        pos = current_state["position"]
        walls = current_state["walls"]
        visited = current_state["visited"]
        steps = current_state["steps"]
        
        # Format walls
        wall_str = "".join([
            "N" if walls["N"] else "x",
            "E" if walls["E"] else "x",
            "W" if walls["W"] else "x",
            "S" if walls["S"] else "x"
        ])
        
        # Format history if available
        history_str = ""
        if history:
            history_str = "\nPrevious moves:\n" + "\n".join([
                f"- {move['move']}: {move['explanation']}"
                for move in history[-3:]  # Only show last 3 moves
            ])
        
        return f"""Current game state:
Position: {pos}
Walls: {wall_str}
Visited cells: {len(visited)}
Steps taken: {steps}{history_str}

What should be the next move? Choose one of: N, E, W, S.
Explain your reasoning and provide a confidence score (0-1).
You must respond in JSON format with the following structure:
{{"move": "N/E/W/S", "explanation": "your reasoning", "confidence": 0.0-1.0}}"""
    
    def get_move(self, 
                current_state: Dict[str, Any],
                history: Optional[list] = None) -> LLMResponse:
        """
        Get the next move from OpenAI's LLM.
        
        Args:
            current_state: Current game state
            history: Optional list of previous moves
        
        Returns:
            LLMResponse containing the move and explanation
        """
        prompt = self._format_state(current_state, history)
        
        try:
            # Use client with request-specific options
            response = self.client.with_options(
                timeout=self.config.timeout
            ).chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Picobot playing agent. Your goal is to explore the environment efficiently. You must respond in JSON format with valid moves and clear explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.model_config.get("max_tokens", 1000),
                response_format={"type": "json_object"},  # Ensure JSON response
                seed=42  # For reproducibility
            )
            
            content = response.choices[0].message.content
            try:
                # Try to parse as JSON first
                move_data = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON response: {str(e)}")
            
            # Validate the move
            if move_data["move"] not in ["N", "E", "W", "S"]:
                raise ValueError(f"Invalid move: {move_data['move']}")
            
            # Update metrics
            self.total_tokens += response.usage.total_tokens
            cost_per_1k = self.model_config.get("cost_per_1k_tokens", 0.03)
            self.total_cost += (response.usage.total_tokens / 1000) * cost_per_1k
            
            return LLMResponse(
                move=move_data["move"],
                explanation=move_data["explanation"],
                confidence=float(move_data.get("confidence", 0.5))
            )
            
        except Exception as e:
            raise RuntimeError(f"Error getting move from OpenAI: {str(e)}") 