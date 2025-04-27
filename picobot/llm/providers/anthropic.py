"""Anthropic provider for Picobot LLM integration."""

import json
import re
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from picobot.llm.base import LLMInterface, Rule
from picobot.llm.prompts import get_prompt

class AnthropicProvider(LLMInterface):
    """Provider implementation for Anthropic models."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        """Initialize the Anthropic provider.
        
        Args:
            model_name: Name of the Anthropic model to use
            temperature: Temperature setting for generation
        """
        super().__init__(model_name, temperature)
        self.client = None
        # Updated model configuration with latest models and correct pricing
        self.model_config = {
            # Original models
            "claude-3-opus-20240229": {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 15.00,
                "cost_per_1k_output_tokens": 75.00
            },
            "claude-3-sonnet-20240229": {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 3.00,
                "cost_per_1k_output_tokens": 15.00
            },
            # Claude 3 Haiku model
            "claude-3-haiku-20240307": {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 0.25,
                "cost_per_1k_output_tokens": 1.25
            },
            # Claude 3.5 models
            "claude-3-5-sonnet-20240620": {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 3.00,
                "cost_per_1k_output_tokens": 15.00
            },
            "claude-3-5-sonnet-20241022": {  # Also available as "claude-3-5-sonnet-latest"
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 3.00,
                "cost_per_1k_output_tokens": 15.00
            },
            "claude-3-5-haiku-20241022": {   # Also available as "claude-3-5-haiku-latest"
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 0.80,
                "cost_per_1k_output_tokens": 4.00
            },
            # Latest Claude 3.7 model
            "claude-3-7-sonnet-20250219": {  # Also available as "claude-3-7-sonnet-latest"
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 3.00,
                "cost_per_1k_output_tokens": 15.00
            }
        }
        self._usage_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0
        }
        
    def initialize(self, api_key: Optional[str] = None) -> None:
        """Initialize the Anthropic client.
        
        Args:
            api_key: Optional API key to use. If not provided, will use environment variable.
        """
        try:
            self.client = Anthropic(api_key=api_key)
            # Test connection with a simple request
            self.client.messages.create(
                model=self.model_name,
                max_tokens=5,
                messages=[{"role": "user", "content": "test"}]
            )
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Anthropic client: {str(e)}")
            
    def generate_rules(self, prompt_name: str = 'basic', num_rules: int = 9) -> List[Rule]:
        """Generate rules using the Anthropic model.
        
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
            raise ConnectionError("Anthropic client not initialized")
            
        try:
            # Get prompt and format it
            prompt = get_prompt(prompt_name)
            prompt = prompt.format(num_rules=num_rules)
            
            # Get model config
            model_config = self.model_config.get(self.model_name, {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 15.00,
                "cost_per_1k_output_tokens": 75.00
            })
            
            # Generate response
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=model_config["max_tokens"],
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Update usage metrics
            self._usage_metrics["prompt_tokens"] += response.usage.input_tokens
            self._usage_metrics["completion_tokens"] += response.usage.output_tokens
            self._usage_metrics["total_tokens"] += response.usage.input_tokens + response.usage.output_tokens
            
            # Updated cost calculation to account for different input/output pricing
            self._usage_metrics["cost"] += (
                response.usage.input_tokens * model_config.get("cost_per_1k_input_tokens", model_config.get("cost_per_1k_tokens", 0.15)) / 1000 +
                response.usage.output_tokens * model_config.get("cost_per_1k_output_tokens", model_config.get("cost_per_1k_tokens", 0.15)) / 1000
            )
            
            # Parse response
            try:
                content = response.content[0].text
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
        # Look for rule-like patterns
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
