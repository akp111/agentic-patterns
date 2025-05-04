from colorama import Fore, Back, Style
from model import ModelFactory, RoleType, ProviderType, ModelType


class Reflection:
    def __init__(self, provider: ProviderType, model_name: str, critique_prompt: str, api_key:str, verbose:bool = False):
        self.system_role = RoleType.System
        self.user_role = RoleType.User
        self.assistant_role = RoleType.Assistant
        self.model_name = model_name
        self.model = ModelFactory(
            api_key=api_key,
            provider= provider ,
            model_name=model_name, 
            verbose=verbose
        )
        self.verbose = verbose
        self.reflection_history = [{
            "role":self.system_role.value,
            "content": critique_prompt+ "\n\nIf you see that all the issues are fixed, please reply with 'Done' only."
        }]
    
    def print_reflection_logs(self, data: str):
        print(Fore.RED + data + Style.RESET_ALL)
    
    def reflect(self, last_generated_info: str):
        self.reflection_history.append({"role": self.user_role.value, "content": last_generated_info})
        critique = self.model.generate(
            prompt=self.reflection_history,
            role=self.user_role
        )
        if self.verbose:
            self.print_reflection_logs(critique)
        self.reflection_history.append({"role": self.assistant_role.value, "content": critique})
        return critique
    
    def return_reflect_history(self):
        return self.reflection_history
