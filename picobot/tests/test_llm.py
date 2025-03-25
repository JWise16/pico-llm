import os
from typing import Dict, Any, Set, Tuple
from ..llm.providers import OpenAIProvider
from ..config.llm_config import LLMConfig
from dotenv import load_dotenv

# Add debugging information
print("Current working directory:", os.getcwd())
print("Environment variables:")
print("OPENAI_API_KEY present:", bool(os.getenv("OPENAI_API_KEY")))
print("OPENAI_API_KEY value:", os.getenv("OPENAI_API_KEY", "Not set")[:5] + "..." if os.getenv("OPENAI_API_KEY") else "Not set")

# Load environment variables
load_dotenv()

print("\nAfter loading .env:")
print("OPENAI_API_KEY present:", bool(os.getenv("OPENAI_API_KEY")))
print("OPENAI_API_KEY value:", os.getenv("OPENAI_API_KEY", "Not set")[:5] + "..." if os.getenv("OPENAI_API_KEY") else "Not set")

class SimplePicobot:
    """A simplified Picobot environment for testing."""
    
    def __init__(self, size: int = 5):
        self.size = size
        self.position = (2, 2)  # Start in middle
        self.visited: Set[Tuple[int, int]] = {self.position}
        self.steps = 0
        
    def get_state(self) -> Dict[str, Any]:
        """Get current game state."""
        x, y = self.position
        return {
            "position": self.position,
            "walls": {
                "N": y == 0,
                "E": x == self.size - 1,
                "W": x == 0,
                "S": y == self.size - 1
            },
            "visited": self.visited,
            "steps": self.steps
        }
    
    def move(self, direction: str) -> bool:
        """Attempt to move in the given direction."""
        x, y = self.position
        new_pos = self.position
        
        if direction == "N" and not self.get_state()["walls"]["N"]:
            new_pos = (x, y - 1)
        elif direction == "E" and not self.get_state()["walls"]["E"]:
            new_pos = (x + 1, y)
        elif direction == "W" and not self.get_state()["walls"]["W"]:
            new_pos = (x - 1, y)
        elif direction == "S" and not self.get_state()["walls"]["S"]:
            new_pos = (x, y + 1)
        else:
            return False
        
        self.position = new_pos
        self.visited.add(new_pos)
        self.steps += 1
        return True
    
    def print_state(self):
        """Print the current state of the environment."""
        print("\nCurrent Environment:")
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x, y) == self.position:
                    row += "🤖 "  # Robot
                elif (x, y) in self.visited:
                    row += "· "  # Visited
                else:
                    row += "□ "  # Unvisited
            print(row)
        print(f"\nSteps: {self.steps}")
        print(f"Visited cells: {len(self.visited)}")

def main():
    # Initialize the environment and LLM
    bot = SimplePicobot()
    config = LLMConfig()
    provider = OpenAIProvider("gpt-3.5-turbo", temperature=0.7, config=config)
    
    # Initialize the LLM
    provider.initialize()
    
    try:
        # Run for a few steps
        for _ in range(10):
            # Get current state
            state = bot.get_state()
            print("\n" + "="*50)
            bot.print_state()
            
            # Get move from LLM
            response = provider.get_move(state)
            print(f"\nLLM Response:")
            print(f"Move: {response.move}")
            print(f"Explanation: {response.explanation}")
            print(f"Confidence: {response.confidence}")
            
            # Execute move
            success = bot.move(response.move)
            if not success:
                print("Move failed - hit a wall!")
            
            # Small delay to make it easier to follow
            import time
            time.sleep(1)
        
        # Print final metrics
        print("\nFinal Metrics:")
        metrics = provider.get_metrics()
        print(f"Total tokens used: {metrics['total_tokens']}")
        print(f"Total cost: ${metrics['total_cost']:.4f}")
        
    finally:
        # Cleanup
        provider.cleanup()

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        print("Current directory:", os.getcwd())
        print("Looking for .env file in:", os.path.join(os.getcwd(), ".env"))
        print("File exists:", os.path.exists(os.path.join(os.getcwd(), ".env")))
        exit(1)
    
    # Run the test
    main() 