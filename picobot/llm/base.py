from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..game.state import State

class LLMResponse(BaseModel):
    """Structured response from the LLM."""
    move: str  # One of ["N", "E", "W", "S"]
    explanation: str  # Explanation of the move
    confidence: float  # Confidence in the move (0-1)

class LLMInterface(ABC):
    """Base interface for LLM providers."""
    
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.total_tokens = 0
        self.total_cost = 0.0
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the LLM provider."""
        pass
    
    @abstractmethod
    def get_next_move(self, state: State) -> Dict[str, Any]:
        """Get the next move from the LLM.
        
        Args:
            state: Current game state
            
        Returns:
            Dictionary containing move, reasoning, and confidence
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the provider."""
        pass
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current usage metrics."""
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "model_name": self.model_name
        }
    
    def reset_metrics(self) -> None:
        """Reset usage metrics."""
        self.total_tokens = 0
        self.total_cost = 0.0 