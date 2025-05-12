import sys
from pathlib import Path

# Add the parent directory to sys.path so Python can find the reflection_pattern module
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(parent_dir))

from tool_pattern import ToolsPattern
from config.env_manager import EnvManager

def main():
    # Initialize the EnvManager to load environment variables
    env_manager = EnvManager()
    
    # Get API keys from EnvManager
    groq_api_key = env_manager.get_groq_api_key(raise_error=True)

    output = ToolsPattern(
     groq_api_key=groq_api_key,
    ).run(
        user_query="Top 5 hacker news summary",
        max_iterations=3,
    )
    print("\n===== FINAL OUTPUT =====")
    print(output)

if __name__ == "__main__":
    main()