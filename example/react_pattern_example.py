import sys
from pathlib import Path

# Add the parent directory to sys.path so Python can find the modules
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(parent_dir))

from react_pattern.react_pattern import ReactPattern
from config.env_manager import EnvManager

def main():
    # Initialize the EnvManager to load environment variables
    env_manager = EnvManager()
    
    # Get API key from EnvManager
    groq_api_key = env_manager.get_groq_api_key(raise_error=True)

    # Create ReAct pattern instance
    react_agent = ReactPattern(
        user_prompt="What's the weather in New York and what are the top 3 news stories today?",
        verbose=True,
        api_key=groq_api_key
    )
    
    # Run the ReAct pattern
    output = react_agent.run()
    
    print("\n===== FINAL OUTPUT =====")
    print(output)

if __name__ == "__main__":
    main()