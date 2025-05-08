import sys
import os
from pathlib import Path

# Add the parent directory to sys.path so Python can find the reflection_pattern module
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(parent_dir))

from dotenv import load_dotenv
from reflection_pattern.reflection_pattern import ReflectionPattern

# Load environment variables
load_dotenv()

def main():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Error: GROQ_API_KEY environment variable not found.")
        print("Please set it in your .env file or environment.")
        return

    rp = ReflectionPattern(
        generation_prompt="You are a pro python developer. Write a merge sort algorithm implementation in Python with proper documentation.",
        reflection_prompt="You are an experienced code reviewer. Review the code and suggest improvements for code efficiency, readability, best practices, and edge cases handling.",
        groq_api_key=groq_api_key,
        verbose=True
    )
    print("Running reflection pattern...")
    result = rp.run()
    print("\n===== FINAL OUTPUT =====")
    print(result)

if __name__ == "__main__":
    main()