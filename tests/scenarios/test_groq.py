#!/usr/bin/env python3
"""Test suite for Groq provider in Picobot."""

import pytest
import os
from dotenv import load_dotenv
from picobot.llm.providers.groq import GroqProvider
from picobot.llm.base import LLMInterface
from picobot.game.environment import Environment
from picobot.robot import Picobot
from picobot.program import Program
import json
from pathlib import Path

# Load environment variables
load_dotenv()

@pytest.fixture
def groq_provider():
    """Create a GroqProvider instance for testing."""
    provider = GroqProvider(model_name="llama-3.3-70b-versatile")
    provider.initialize()
    return provider

def test_groq_initialization(groq_provider):
    """Test that GroqProvider initializes correctly"""
    assert isinstance(groq_provider, LLMInterface)
    assert groq_provider.model_name == "llama-3.3-70b-versatile"
    assert groq_provider.temperature == 0.7

def test_groq_rule_generation(groq_provider):
    """Test that GroqProvider can generate rules"""
    rules = groq_provider.generate_rules(prompt_name='basic', num_rules=9)
    assert len(rules) > 0
    for rule in rules:
        assert hasattr(rule, 'state')
        assert hasattr(rule, 'pattern')
        assert hasattr(rule, 'move')
        assert hasattr(rule, 'next_state')

def test_groq_usage_metrics(groq_provider):
    """Test that usage metrics are tracked correctly"""
    # Generate some rules to trigger usage
    groq_provider.generate_rules(prompt_name='basic', num_rules=9)
    
    metrics = groq_provider.get_usage_metrics()
    assert 'prompt_tokens' in metrics
    assert 'completion_tokens' in metrics
    assert 'total_tokens' in metrics
    assert 'cost' in metrics
    assert metrics['total_tokens'] > 0
    assert metrics['cost'] >= 0

def test_groq_cleanup(groq_provider):
    """Test that cleanup works correctly"""
    groq_provider.cleanup()
    assert groq_provider.client is None 