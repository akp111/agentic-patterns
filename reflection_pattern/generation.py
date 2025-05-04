from colorama import Fore, Back, Style
from model import ModelFactory, RoleType, ProviderType, ModelType

class Generation:
    def __init__(self, prompt: str, provider: ProviderType = ProviderType.Groq, model_name: ModelType = ModelType.Llama3_3_70B_Versatile, api_key: str = None, verbose: bool = False):
        self.prompt = prompt
        self.role = RoleType.System
        self.model = ModelFactory(
            api_key=api_key,
            provider=provider, 
            model_name=model_name, 
            verbose=verbose
        )
        self.generate_history = []
        self.generate_history.append({"role": self.role.value, "content": prompt})
        self.verbose = verbose
    
    def __str__(self):
        return "Generation Module"
    
    def print_generation_log(self, data: str):
        print(Fore.GREEN + data + Style.RESET_ALL)
    
    def generate(self, prompt: str = None):
        current_prompt = prompt if prompt is not None else self.prompt
        
        if prompt is not None:
            self.generate_history.append({"role": self.role.value, "content": current_prompt})
        
        output = self.model.generate(current_prompt, self.role)
        
        if self.verbose:
            self.print_generation_log(output)
            
        self.generate_history.append({"role": "assistant", "content": output})
        return output
    
    def get_generation_history(self):
        return self.generate_history

