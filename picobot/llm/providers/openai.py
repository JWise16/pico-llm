"""OpenAI provider for Picobot LLM integration."""

import json
import os
import re
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv
from ..base import LLMInterface, Rule
from ..prompts import get_prompt

class OpenAIProvider(LLMInterface):
    """OpenAI provider implementation."""
    
    def __init__(self, model_name: str = "gpt-4.1-2025-04-14", temperature: float = 0.2):
        """Initialize OpenAI provider.
        
        Args:
            model_name: Name of the model to use
            temperature: Temperature setting for generation
        """
        super().__init__(model_name, temperature)
        self.client = None
        self.model_config = {
            # Latest GPT-4.1 models
            "gpt-4.1-2025-04-14": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 2.00,
                "cost_per_1k_output_tokens": 8.00
            },
            "gpt-4.1-mini-2025-04-14": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 0.40,
                "cost_per_1k_output_tokens": 1.60
            },
            "gpt-4.1-nano-2025-04-14": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 0.10,
                "cost_per_1k_output_tokens": 0.40
            },
            # Previous models maintained for backward compatibility
            "gpt-4": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 30.00,
                "cost_per_1k_output_tokens": 60.00
            },
            "gpt-3.5-turbo": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 0.50,
                "cost_per_1k_output_tokens": 1.50
            },
            # New o-series models
            "o3-mini-2025-01-31": {
                "max_tokens": 8000,
                "cost_per_1k_input_tokens": 1.10,
                "cost_per_1k_output_tokens": 4.40
            }
        }
        self._usage_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0
        }
        
    def initialize(self, api_key: Optional[str] = None) -> None:
        """Initialize OpenAI client.
        
        Args:
            api_key: Optional API key to use. If not provided, will use environment variable.
            
        Raises:
            ConnectionError: If initialization fails
        """
        try:
            load_dotenv()
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found")
            
            self.client = openai.OpenAI(api_key=api_key)
            
            # Validate model name
            if self.model_name not in self.model_config:
                print(f"Warning: {self.model_name} not in model_config - using default pricing")
                
            # Test connection with appropriate token parameter
            if self.model_name.startswith("o3"):
                self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_completion_tokens=5
                )
            else:
                self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
        except Exception as e:
            raise ConnectionError(f"Initialization failed: {str(e)}")

    def generate_rules(self, prompt_name: str = 'basic', num_rules: int = 9) -> List[Rule]:
        """Generate rules using OpenAI."""
        if not self.client:
            raise ConnectionError("Client not initialized")
            
        try:
            prompt = get_prompt(prompt_name).format(num_rules=num_rules)
            model_config = self.model_config.get(self.model_name, {
                "max_tokens": 4000,
                "cost_per_1k_input_tokens": 2.00,
                "cost_per_1k_output_tokens": 8.00
            })
            
            # Define the function schema for rule generation
            functions = [
                {
                    "name": "generate_picobot_rules",
                    "description": "Generate rules for Picobot navigation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rules": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "state": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 4,
                                            "description": "Current state (0-4)"
                                        },
                                        "pattern": {
                                            "type": "string",
                                            "pattern": "^[NSEWx]{4}$",
                                            "description": "Wall pattern (NSEWx)"
                                        },
                                        "move": {
                                            "type": "string",
                                            "enum": ["N", "S", "E", "W"],
                                            "description": "Move direction"
                                        },
                                        "next_state": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 4,
                                            "description": "Next state (0-4)"
                                        }
                                    },
                                    "required": ["state", "pattern", "move", "next_state"]
                                }
                            }
                        },
                        "required": ["rules"]
                    }
                }
            ]
            
            # Configure parameters based on model type
            params = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a Picobot rule generator implementing a wall-following strategy. You must respond with a VALID JSON object containing a "rules" array. Each rule in the array must have these exact fields:
- state: number (0-4)
- pattern: string (4 chars, NSEWx)
- move: string (N, E, W, S)
- next_state: number (0-4)

WALL FOLLOWING STRATEGY:
1. State 0: Initial state - Find a wall
   - If no walls: Move east until finding a wall
   - If wall found: Move to state 1
   - If blocked: Try alternate directions

2. State 1: Follow right wall
   - Keep wall on right side
   - If wall on right: Move forward
   - If no wall on right: Turn right
   - If blocked: Move to state 2

3. State 2: Handle corners and obstacles
   - If corner: Turn left and continue
   - If dead end: Turn around
   - After handling: Return to state 1

4. State 3: Recovery from stuck
   - If stuck: Try moving away from current wall
   - If path found: Return to state 0
   - If still stuck: Move to state 4

5. State 4: Special cases
   - Handle complex wall patterns
   - Try alternate directions
   - Return to state 0 when clear

MOVEMENT RULES:
1. Right wall following:
   - If wall on E: Move S
   - If wall on S: Move W
   - If wall on W: Move N
   - If wall on N: Move E

2. Corner handling:
   - If NE walls: Move S
   - If SE walls: Move W
   - If SW walls: Move N
   - If NW walls: Move E

3. Dead end handling:
   - If NSE walls: Move W
   - If NSW walls: Move E
   - If NEW walls: Move S
   - If ESW walls: Move N

IMPORTANT RULES:
1. The response must be VALID JSON - no comments allowed
2. Do not include any explanatory text before or after the JSON
3. Each rule must be a complete object with all required fields
4. All field names must be in quotes
5. Use only the specified field names and types
6. Do not truncate the response - all rules must be complete
7. Do not use any line comments (//) or block comments (/* */)
8. Do not use any trailing commas
9. Do not use any whitespace in patterns
10. Generate rules for ALL required patterns

Example response format:
{
  "rules": [
    {
      "state": 0,
      "pattern": "xxxx",
      "move": "E",
      "next_state": 0
    },
    {
      "state": 0,
      "pattern": "xExx",
      "move": "S",
      "next_state": 1
    }
  ]
}"""
                    },
                    {"role": "user", "content": prompt}
                ],
                "functions": functions,
                "function_call": {"name": "generate_picobot_rules"},
                "response_format": { "type": "json_object" }
            }
            
            # Add token limit parameter
            token_param = "max_completion_tokens" if self.model_name.startswith("o3") else "max_tokens"
            params[token_param] = model_config["max_tokens"]
            
            # Add temperature only for non-o3 models
            if not self.model_name.startswith("o3"):
                params["temperature"] = self.temperature
            
            response = self.client.chat.completions.create(**params)
            
            # Get response content from function call
            if response.choices[0].message.function_call:
                content = response.choices[0].message.function_call.arguments
            else:
                content = response.choices[0].message.content
                
            print("\nRaw response:")
            print("="*50)
            print(content)
            print("="*50)
            print("\nResponse type:", type(content))
            print("Response length:", len(content))
            
            # Parse JSON response
            try:
                data = json.loads(content)
                print("\nParsed JSON:")
                print(json.dumps(data, indent=2))
                
                # Extract rules from the response
                rules_data = data.get("rules", [])
                if not rules_data:
                    raise ValueError("No rules found in response")
                
                # Validate each rule
                rules = []
                for rule in rules_data:
                    # Validate required fields
                    if not all(k in rule for k in ["state", "pattern", "move", "next_state"]):
                        raise ValueError(f"Missing required fields in rule: {rule}")
                    
                    # Validate field types and values
                    if not isinstance(rule["state"], int) or not (0 <= rule["state"] <= 4):
                        raise ValueError(f"Invalid state value in rule: {rule}")
                    if not isinstance(rule["pattern"], str) or not re.match(r"^[NSEWx]{4}$", rule["pattern"]):
                        raise ValueError(f"Invalid pattern in rule: {rule}")
                    if not isinstance(rule["move"], str) or rule["move"] not in ["N", "S", "E", "W"]:
                        raise ValueError(f"Invalid move in rule: {rule}")
                    if not isinstance(rule["next_state"], int) or not (0 <= rule["next_state"] <= 4):
                        raise ValueError(f"Invalid next_state value in rule: {rule}")
                    
                    rules.append(Rule(
                        state=rule["state"],
                        pattern=rule["pattern"],
                        move=rule["move"],
                        next_state=rule["next_state"]
                    ))
                
                return rules
                
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON decode error: {str(e)}")
            except Exception as e:
                raise ValueError(f"Error parsing response: {str(e)}")
                
        except Exception as e:
            raise ValueError(f"Generation failed: {str(e)}")
            
    def cleanup(self) -> None:
        """Clean up resources."""
        self.client = None
        
    def get_usage_metrics(self) -> Dict:
        """Get usage metrics."""
        return self._usage_metrics.copy()
