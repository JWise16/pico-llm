import pytest
import os
from dotenv import load_dotenv
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.llm.base import LLMInterface
from picobot.game.environment import Environment
from picobot.robot import Picobot
import random

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def anthropic_provider():
    return AnthropicProvider()

@pytest.fixture
def environment():
    return Environment(width=5, height=5)

def test_anthropic_initialization(anthropic_provider):
    """Test that AnthropicProvider initializes correctly"""
    assert isinstance(anthropic_provider, LLMInterface)
    assert anthropic_provider.model_name == "claude-3-opus-20240229"
    assert anthropic_provider.temperature == 0.7

def test_rule_generation(anthropic_provider):
    """Test that AnthropicProvider can generate valid rules"""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    
    # Initialize the provider with API key
    anthropic_provider.initialize(api_key=api_key)
    
    try:
        # Generate rules
        rules = anthropic_provider.generate_rules(prompt_name='basic', num_rules=9)
        
        # Validate rules
        assert len(rules) > 0
        for rule in rules:
            assert hasattr(rule, 'state')
            assert hasattr(rule, 'pattern')
            assert hasattr(rule, 'move')
            assert hasattr(rule, 'next_state')
            
            # Validate pattern format
            assert len(rule.pattern) == 4
            assert all(c in 'NSEWx' for c in rule.pattern)
            
            # Validate move
            assert rule.move in ['N', 'S', 'E', 'W']
            
            # Validate state transitions
            assert isinstance(rule.state, int)
            assert isinstance(rule.next_state, int)
            assert 0 <= rule.state <= 9
            assert 0 <= rule.next_state <= 9
        
        # Get usage metrics
        metrics = anthropic_provider.get_usage_metrics()
        assert metrics['total_tokens'] > 0
        assert metrics['cost'] >= 0
        
    finally:
        # Cleanup
        anthropic_provider.cleanup()

def test_wall_following_rules(anthropic_provider):
    """Test that wall-following strategy generates appropriate rules"""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    
    # Initialize the provider with API key
    anthropic_provider.initialize(api_key=api_key)
    
    try:
        # Generate rules with wall-following strategy
        rules = anthropic_provider.generate_rules(prompt_name='wall_following', num_rules=9)
        
        # Basic validation
        assert len(rules) > 0
        
        # Check for wall-following patterns
        wall_patterns = set()
        for rule in rules:
            # Add patterns that involve walls
            if any(c in 'NSEW' for c in rule.pattern):
                wall_patterns.add(rule.pattern)
        
        # Should have some patterns that deal with walls
        assert len(wall_patterns) > 0, "No wall-following patterns found"
        
        # Get usage metrics
        metrics = anthropic_provider.get_usage_metrics()
        assert metrics['total_tokens'] > 0
        assert metrics['cost'] >= 0
        
    finally:
        # Cleanup
        anthropic_provider.cleanup() 