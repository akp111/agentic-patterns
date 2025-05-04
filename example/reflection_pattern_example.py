from dotenv import load_dotenv
import os
from model.model_enums import ProviderType, ModelType
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
        api_key=groq_api_key,
        iterations=3, 
        verbose=True,
        provider=ProviderType.Groq,
        model_name=ModelType.Llama3_3_70B_Versatile# Assuming you want to use the Groq provider
    )
    
    print("Running reflection pattern...")
    result = rp.run()
    print("\n===== FINAL OUTPUT =====")
    print(result)

if __name__ == "__main__":
    main()