from reflection_pattern import ReflectionPattern
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    rp = ReflectionPattern(
        generation_prompt="You are a pro python developer … merge sort …",
        reflection_prompt="You are an experienced … recommending improvements …",
        verbose=True,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    print("Final output",rp.run())

main()