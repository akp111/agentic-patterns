from . import model_enums
from . import groq
from .model_base import ModelBase
from dataclasses import dataclass

@dataclass
class ModelFactory:
    api_key: str
    provider: model_enums.ProviderType = model_enums.ProviderType.Groq
    model_name: model_enums.ModelType = model_enums.ModelType.Llama3_3_70B_Versatile
    verbose: bool = False
    model: any = None
    
    def __post_init__(self)-> ModelBase:
        print(self)
        if self.provider == model_enums.ProviderType.Groq:
            self.model = groq.GroqModel(
                model_name=self.model_name,
                api_key=self.api_key,
                verbose=self.verbose
            )
        print(self)
        return self.model
    
    def generate(self, prompt: list, role: model_enums.RoleType):
        """
        Delegate the generate method call to the underlying model.
        """
        if self.model:
            return self.model.generate(prompt, role)
        else:
            raise ValueError("Model is not initialized")
