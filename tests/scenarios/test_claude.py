import pytest
from picobot.llm.providers.anthropic import AnthropicProvider
from picobot.llm.base import LLMInterface
from picobot.game.environment import Environment
from picobot.game.state import State

@pytest.fixture
def anthropic_provider():
    return AnthropicProvider()

@pytest.fixture
def environment():
    return Environment(width=5, height=5)

def test_anthropic_initialization(anthropic_provider):
    """Test that AnthropicProvider initializes correctly"""
    assert isinstance(anthropic_provider, LLMInterface)
    assert anthropic_provider.model == "claude-3-7-sonnet-20250219"
    assert anthropic_provider.temperature == 0.7

def test_anthropic_move_generation(anthropic_provider, environment):
    """Test that AnthropicProvider generates valid moves"""
    state = State(environment)
    response = anthropic_provider.get_next_move(state)
    
    assert isinstance(response, dict)
    assert "move" in response
    assert "reasoning" in response
    assert "confidence" in response
    assert response["move"] in ["North", "South", "East", "West"]
    assert 0 <= response["confidence"] <= 1

def test_anthropic_wall_avoidance(anthropic_provider, environment):
    """Test that AnthropicProvider avoids walls"""
    # Set up a wall in front of the bot
    environment.set_cell(0, 1, True)  # Wall to the north
    state = State(environment)
    
    response = anthropic_provider.get_next_move(state)
    assert response["move"] != "North" 