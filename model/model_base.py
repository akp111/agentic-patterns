from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any, Union, Dict, List, TypedDict

from . import model_enums

class MessageContent(TypedDict):
    role: str
    content: str


PromptType = Union[str, List[MessageContent]]

@dataclass
class ModelBase(ABC):
    api_key: str
    model_name: model_enums.ModelType
    verbose: bool = False
    model: any = None
    role: Optional[model_enums.RoleType] = None
    
    def __post_init__(self):
        """
        Post-initialization method to set up the model.
        :return: None
        """
        self.init_model()
        if self.verbose:
            print(f"Model initialized with name: {self.model_name}, role: {self.role}")
    
    @abstractmethod
    def init_model(self):
        """
        Initialize the model with the given parameters.
        :return: None
        """
        pass
    
    @abstractmethod
    def generate(self, prompt: PromptType = None, role: Optional[model_enums.RoleType] = None):
        """
        Generate a response from the model.
        :param prompt: The prompt to generate a response for. Can be a string or a list of message objects.
        :param role: The role type for the request (used only if prompt is a string).
        :return: The generated response.
        """
        pass