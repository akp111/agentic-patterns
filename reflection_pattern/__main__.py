from . import reflection_pattern
    

if __name__ == "__main__":
    reflection_instance = reflection_pattern.ReflectionPattern(generation_prompt="You are a pro python developer who is tasked to develop high quality code. Your task to implement merge sort in python.", reflection_prompt="You are an experienced software developer and scientist. You are tasked with generating critique and recommending improvements as pointers.")
    output = reflection_instance.run()
    print("final output:", output)