from . import generation
from . import reflection
from time import sleep
from model import ProviderType, ModelType


class ReflectionPattern:
    def __init__(self, provider: ProviderType, model_name: ModelType, generation_prompt: str, reflection_prompt: str, api_key: str, iterations: int = 3, verbose: bool = False):
        self.generation_prompt = generation_prompt
        self.reflection_prompt = reflection_prompt
        self.iterations = iterations
        self.verbose = verbose
        self.gen = generation.Generation(
            prompt=generation_prompt, 
            model_name=model_name, 
            api_key=api_key, 
            verbose=verbose,
            provider=provider
        )
        self.reflect = reflection.Reflection(
            model_name=model_name, 
            critique_prompt=reflection_prompt, 
            api_key=api_key, 
            verbose=verbose,
            provider=provider
        )

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