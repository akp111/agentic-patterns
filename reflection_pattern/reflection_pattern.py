from . import generation
from . import reflection
from time import sleep


class ReflectionPattern:
    def __init__(self, generation_prompt: str, reflection_prompt: str, groq_api_key: str, iterations: int = 3, verbose: bool = False):
        self.generation_prompt = generation_prompt
        self.reflection_prompt = reflection_prompt
        self.iterations = iterations
        self.verbose = verbose
        self.gen = generation.Generation(prompt=generation_prompt, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key, verbose=verbose)
        self.reflect = reflection.Reflection(model_name="llama-3.3-70b-versatile", critique_prompt=reflection_prompt, groq_api_key=groq_api_key, verbose=verbose)

    def run(self):
        critique = None
        output = self.gen.generate()
        sleep(1)
        while len(self.gen.get_generation_history()) < self.iterations and critique != "Done":
            if self.verbose:
                print("Iteration: ", len(self.gen.get_generation_history()))
            critique = self.reflect.reflect(output)
            sleep(1)
            output = self.gen.generate(prompt=critique)
            sleep(1)
        
        return output