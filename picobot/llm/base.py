from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..game.state import State
from dataclasses import dataclass

@dataclass
class Rule:
    """Represents a Picobot rule."""
    state: int
    pattern: str
    move: str
    next_state: int
    
    def __post_init__(self):
        """Validate rule fields."""
        if not (0 <= self.state <= 4):
            raise ValueError(f"Invalid state: {self.state}")
        if not (0 <= self.next_state <= 4):
            raise ValueError(f"Invalid next state: {self.next_state}")
        if len(self.pattern) != 4:
            raise ValueError(f"Invalid pattern length: {len(self.pattern)}")
        if not all(c in 'NSEWx' for c in self.pattern):
            raise ValueError(f"Invalid pattern characters: {self.pattern}")
        if self.move not in 'NSEW':
            raise ValueError(f"Invalid move: {self.move}")

class LLMResponse(BaseModel):
    """Structured response from the LLM."""
    move: str  # One of ["N", "E", "W", "S"]
    explanation: str  # Explanation of the move
    confidence: float  # Confidence in the move (0-1)

class LLMInterface(ABC):
    """Base interface for LLM providers."""
    
    def __init__(self, model_name: str, temperature: float = 0.7):
        """Initialize the LLM interface.
        
        Args:
            model_name: Name of the model to use
            temperature: Temperature setting for generation
        """
        self.model_name = model_name
        self.temperature = temperature
        self._usage_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0
        }
    
    @abstractmethod
    def initialize(self, api_key: Optional[str] = None) -> None:
        """Initialize the LLM client.
        
        Args:
            api_key: Optional API key to use. If not provided, will use environment variable.
            
        Raises:
            ConnectionError: If initialization fails
        """
        pass
    
    @abstractmethod
    def generate_rules(self, prompt_name: str = 'basic', num_rules: int = 9) -> List[Rule]:
        """Generate rules using the LLM.
        
        Args:
            prompt_name: Name of the prompt to use
            num_rules: Number of rules to generate
            
        Returns:
            List of generated rules
            
        Raises:
            ValueError: If the prompt name is invalid
            ConnectionError: If there are API connection issues
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources."""
        pass
    
    def get_usage_metrics(self) -> Dict:
        """Get usage metrics.
        
        Returns:
            Dictionary containing usage metrics
        """
        return self._usage_metrics.copy()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current usage metrics."""
        return {
            "total_tokens": self._usage_metrics["total_tokens"],
            "total_cost": self._usage_metrics["cost"],
            "model_name": self.model_name
        }
    
    def reset_metrics(self) -> None:
        """Reset usage metrics."""
        self._usage_metrics["total_tokens"] = 0
        self._usage_metrics["cost"] = 0.0 