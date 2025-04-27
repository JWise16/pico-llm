"""Test comparison of different prompts with Claude."""

import os
from dotenv import load_dotenv
import pytest
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.llm.prompts import (
    BASIC_PROMPT,
    WALL_FOLLOWING_PROMPT,
    SYSTEMATIC_PROMPT,
    ENGLISH_PROMPT,
    SPIRAL_PROMPT,
    SNAKE_PROMPT,
    ZIGZAG_PROMPT
)

# Load environment variables
load_dotenv()

# Get API key from environment
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

@pytest.fixture
def anthropic_provider():
    """Create an AnthropicProvider instance for testing."""
    provider = AnthropicProvider(
        model_name="claude-3-sonnet-20240229",
        temperature=0.7
    )
    # Initialize the client
    provider.initialize()
    return provider

def test_prompt_initialization(anthropic_provider):
    """Test that the provider initializes correctly."""
    assert anthropic_provider.model_name == "claude-3-sonnet-20240229"
    assert anthropic_provider.temperature == 0.7
    assert anthropic_provider.client is not None

def test_basic_prompt(anthropic_provider):
    """Test rule generation with basic prompt."""
    rules = anthropic_provider.generate_rules('basic')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_wall_following_prompt(anthropic_provider):
    """Test rule generation with wall following prompt."""
    rules = anthropic_provider.generate_rules('wall_following')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_systematic_prompt(anthropic_provider):
    """Test rule generation with systematic prompt."""
    rules = anthropic_provider.generate_rules('systematic')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_english_prompt(anthropic_provider):
    """Test rule generation with english prompt."""
    rules = anthropic_provider.generate_rules('english')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_spiral_prompt(anthropic_provider):
    """Test rule generation with spiral prompt."""
    rules = anthropic_provider.generate_rules('spiral')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_snake_prompt(anthropic_provider):
    """Test rule generation with snake prompt."""
    rules = anthropic_provider.generate_rules('snake')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_zigzag_prompt(anthropic_provider):
    """Test rule generation with zigzag prompt."""
    rules = anthropic_provider.generate_rules('zigzag')
    assert isinstance(rules, list)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_usage_metrics(anthropic_provider):
    """Test that usage metrics are being tracked."""
    # Generate rules with each prompt
    prompts = [
        'basic',
        'wall_following',
        'systematic',
        'english',
        'spiral',
        'snake',
        'zigzag'
    ]
    
    for prompt in prompts:
        anthropic_provider.generate_rules(prompt)
    
    metrics = anthropic_provider.get_usage_metrics()
    assert metrics['prompt_tokens'] > 0
    assert metrics['completion_tokens'] > 0
    assert metrics['total_tokens'] > 0
    assert metrics['cost'] > 0 