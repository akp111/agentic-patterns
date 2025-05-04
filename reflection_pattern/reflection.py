from groq import Groq
from colorama import Fore,Back, Style\
    
class Reflection:
    def __init__(self, model_name: str, critique_prompt: str, groq_api_key:str, verbose:bool = False):
        self.model = Groq(api_key=groq_api_key)
        self.model_name = model_name
        self.system_role = "system"
        self.user_role = "user"
        self.verbose = verbose
        self.reflection_history = [{
            "role":self.system_role,
            "content": critique_prompt+ "\n\nIf you see that all the issues are fixed, please reply with 'Done' only."
        }]
    
    def print_reflection_logs(self, data: str):
        print(Fore.RED + data + Style.RESET_ALL)
    
    def reflect(self, last_generated_info: str):
        self.reflection_history.append({"role":self.user_role, "content": last_generated_info})
        critique = self.model.chat.completions.create(
            messages=self.reflection_history,
            model=self.model_name
        ).choices[0].message.content
        if self.verbose:
            self.print_reflection_logs(critique)
        self.reflection_history.append({"role": "assistant", "content": critique})
        return critique
    
    def return_reflect_history(self):
        return self.reflection_history
        