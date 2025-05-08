from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolsBase(ABC):
    name: str
    tool: Any = None
    
    def __post_init__(self):
        """
        Post-initialization method to set up the tool.
        :return: None
        """
        self.init_tool()
    
    @abstractmethod
    def init_tool(self, **kwargs):
        """
        Initialize the tool
        """
        pass
    
    @abstractmethod
    def run(self, **kwargs):
        """
        Call the tool function
        """
        pass
    
    @abstractmethod
    def get_tool_parameters(self):
        """
        Get the parameters of the tool
        """
        pass