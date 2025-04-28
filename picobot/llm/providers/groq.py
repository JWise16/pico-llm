"""Groq Cloud provider for Picobot LLM integration."""

import json
import os
import re
from typing import List, Dict, Any, Optional
from groq import Groq
from picobot.llm.base import LLMInterface, Rule
from picobot.llm.prompts import get_prompt

class GroqProvider(LLMInterface):
    """Provider implementation for Groq Cloud models."""
    
    def __init__(self, model_name: str = "mixtral-8x7b-32768", temperature: float = 0.7):
        """Initialize the Groq provider.
        
        Args:
            model_name: Name of the Groq model to use
            temperature: Temperature setting for generation
        """
        super().__init__(model_name, temperature)
        self.client = None
        self.model_config = {
            # Llama 4 models (NEW, as of April 2025)
            "llama-4-scout-17bx16e": {
                "max_tokens": 128000,
                "cost_per_1k_input_tokens": 0.11,
                "cost_per_1k_output_tokens": 0.34
            },
            "llama-4-maverick-17bx128e": {
                "max_tokens": 128000,
                "cost_per_1k_input_tokens": 0.20,
                "cost_per_1k_output_tokens": 0.60
            },
            # Llama 3.3 and 3.1 models
            "llama-3.3-70b-versatile": {
                "max_tokens": 32768,
                "cost_per_1k_input_tokens": 0.59,
                "cost_per_1k_output_tokens": 0.79
            },
            "llama-3.1-8b-instant": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.05,
                "cost_per_1k_output_tokens": 0.08
            },
            # Llama Guard
            "llama-guard-3-8b": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.20,
                "cost_per_1k_output_tokens": 0.20
            },
            # Llama 3 legacy
            "llama3-70b-8192": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.59,
                "cost_per_1k_output_tokens": 0.79
            },
            "llama3-8b-8192": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.05,
                "cost_per_1k_output_tokens": 0.08
            },
            # Gemma
            "gemma2-9b-it": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.20,
                "cost_per_1k_output_tokens": 0.20
            },
            "deepseek-r1-distill-llama-70b": {
                "max_tokens": 8192,
                "cost_per_1k_input_tokens": 0.20,
                "cost_per_1k_output_tokens": 0.20
            }
        }

        self._usage_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0
        }
        
    def initialize(self, api_key: Optional[str] = None) -> None:
        """Initialize the Groq client.
        
        Args:
            api_key: Optional API key to use. If not provided, will use environment variable.
            
        Raises:
            ConnectionError: If initialization fails
        """
        try:
            # Get API key from parameter or environment
            api_key = api_key or os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not found")
            
            self.client = Groq(api_key=api_key)
            
            # Test connection with a simple request
            self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Groq client: {str(e)}")
            
    def generate_rules(self, prompt_name: str = 'basic', num_rules: int = 9) -> List[Rule]:
        """Generate rules using the Groq model.
        
        Args:
            prompt_name: Name of the prompt to use
            num_rules: Number of rules to generate
            
        Returns:
            List of generated rules
            
        Raises:
            ValueError: If the prompt name is invalid
            ConnectionError: If there are API connection issues
        """
        if not self.client:
            raise ConnectionError("Groq client not initialized")
            
        try:
            # Get prompt and format it
            prompt = get_prompt(prompt_name)
            prompt = prompt.format(num_rules=num_rules)
            
            # Get model config
            model_config = self.model_config.get(self.model_name, {
                "max_tokens": 32768,
                "cost_per_1k_input_tokens": 0.79,
                "cost_per_1k_output_tokens": 0.79
            })
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=model_config["max_tokens"]
            )
            
            # Update usage metrics
            self._usage_metrics["prompt_tokens"] += response.usage.prompt_tokens
            self._usage_metrics["completion_tokens"] += response.usage.completion_tokens
            self._usage_metrics["total_tokens"] += response.usage.total_tokens
            self._usage_metrics["cost"] += (
                response.usage.prompt_tokens * model_config["cost_per_1k_input_tokens"] / 1000 +
                response.usage.completion_tokens * model_config["cost_per_1k_output_tokens"] / 1000
            )
            
            # Parse response
            try:
                content = response.choices[0].message.content
                print("\nRaw response:")
                print(content)
                
                # Try to extract JSON from the response
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    data = json.loads(json_str)
                    print("\nParsed JSON:")
                    print(json.dumps(data, indent=2))
                    
                    # Extract rules from the response
                    rules_data = data.get("rules", [])
                    if not rules_data:
                        raise ValueError("No rules found in response")
                    
                    rules = []
                    for rule in rules_data:
                        try:
                            rules.append(Rule(
                                state=rule["state"],
                                pattern=rule["pattern"],
                                move=rule["move"],
                                next_state=rule["next_state"]
                            ))
                        except (KeyError, ValueError) as e:
                            print(f"Invalid rule format: {rule}, error: {str(e)}")
                    return rules
                else:
                    raise ValueError("No JSON object found in response")
                    
            except json.JSONDecodeError as e:
                print(f"\nJSON decode error: {str(e)}")
                # Try to salvage partial rules
                rules = self._extract_individual_rules(content)
                if rules:
                    return rules
                raise ValueError("Failed to parse rules from response")
                
        except Exception as e:
            raise ConnectionError(f"Failed to generate rules: {str(e)}")
            
    def _extract_individual_rules(self, content: str) -> List[Rule]:
        """Extract individual rules from potentially malformed JSON response.
        
        Args:
            content: Response content to parse
            
        Returns:
            List of extracted rules
        """
        rules = []
        # Look for rule-like patterns (same regex as other providers)
        pattern = r'{\s*"state"\s*:\s*(\d+)\s*,\s*"pattern"\s*:\s*"([NSEWx]{4})"\s*,\s*"move"\s*:\s*"([NSEW])"\s*,\s*"next_state"\s*:\s*(\d+)\s*}'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            try:
                rules.append(Rule(
                    state=int(match.group(1)),
                    pattern=match.group(2),
                    move=match.group(3),
                    next_state=int(match.group(4))
                ))
            except (ValueError, IndexError):
                continue
                
        return rules
        
    def cleanup(self) -> None:
        """Clean up resources."""
        self.client = None
        
    def get_usage_metrics(self) -> Dict:
        """Get usage metrics.
        
        Returns:
            Dictionary containing usage metrics
        """
        return self._usage_metrics.copy()
