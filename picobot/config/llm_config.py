from typing import Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    
    # OpenAI configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_models: Dict[str, Any] = {
        "gpt-4-0125-preview": {"max_tokens": 1000, "cost_per_1k_tokens": 0.03},
        "gpt-4-turbo-preview": {"max_tokens": 1000, "cost_per_1k_tokens": 0.03},
        "gpt-4": {"max_tokens": 1000, "cost_per_1k_tokens": 0.03},
        "gpt-3.5-turbo-0125": {"max_tokens": 1000, "cost_per_1k_tokens": 0.002},
        "gpt-3.5-turbo": {"max_tokens": 1000, "cost_per_1k_tokens": 0.002}
    }
    
    # Anthropic configuration
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_models: Dict[str, Any] = {
        "claude-3-opus-20240229": {"max_tokens": 1000, "cost_per_1k_tokens": 0.015},
        "claude-3-sonnet-20240229": {"max_tokens": 1000, "cost_per_1k_tokens": 0.003}
    }
    
    # General settings
    default_temperature: float = 0.7
    max_retries: int = 3
    timeout: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8" 