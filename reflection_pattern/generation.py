from groq import Groq
from colorama import Fore, Back, Style

class Generation:
    def __init__(self, prompt: str, model_name: str, groq_api_key: str, verbose: bool = False):
        self.prompt = prompt
        self.model = Groq(api_key=groq_api_key)
        self.model_name = model_name
        self.generate_history = []
        self.role = "system"
        self.generate_history.append({"role":self.role, "content":prompt})
        self.verbose = verbose
    
    def __str__(self):
        return "Generation Module"
    
    def print_generation_log(self, data: str):
        print(Fore.GREEN + data + Style.RESET_ALL)
    
    def generate(self, prompt: str = None):
        if prompt is not None:
            self.generate_history.append({"role": self.role, "content": prompt})
        output = self.model.chat.completions.create(
            messages=self.generate_history,
            model=self.model_name
        ).choices[0].message.content
        if self.verbose:
            self.print_generation_log((output))
        self.generate_history.append({"role": self.role, "content": output})
        return output
    
    def get_generation_history(self):
        return self.generate_history
        
        