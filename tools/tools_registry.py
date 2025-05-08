from typing import Dict, Any, Type, List, Optional
import inspect

# Use relative import instead of absolute import with sys.path manipulation
from .tools_base import ToolsBase

class ToolsRegistry:
    """
    A registry for tool classes that can be used by AI agents.
    This registry allows for dynamic registration and retrieval of tool implementations.
    """
    _registry: Dict[str, Type[ToolsBase]] = {}
    
    @classmethod
    def register(cls, tool_class: Type[ToolsBase]) -> None:
        """
        Register a tool class in the registry
        
        Args:
            tool_class: The tool class to register (must inherit from ToolsBase)
        """
        cls._registry[tool_class.__name__] = tool_class
    
    @classmethod
    def get_tool_class(cls, tool_name: str) -> Optional[Type[ToolsBase]]:
        """
        Get a tool class by name
        
        Args:
            tool_name: The name of the tool class to retrieve
            
        Returns:
            The tool class if found, None otherwise
        """
        return cls._registry.get(tool_name)
    
    @classmethod
    def list_available_tools(cls) -> List[str]:
        """
        List all available tool names
        
        Returns:
            A list of tool class names that are registered
        """
        return list(cls._registry.keys())
    
    @classmethod
    def create_tool(cls, tool_name: str, **kwargs) -> Optional[ToolsBase]:
        """
        Create an instance of a tool by name
        
        Args:
            tool_name: The name of the tool class to create
            **kwargs: Arguments to pass to the tool's constructor
            
        Returns:
            An instance of the requested tool, or None if the tool wasn't found
        """
        tool_class = cls.get_tool_class(tool_name)
        if tool_class:
            return tool_class(**kwargs)
        return None
    
   
def register_tool(tool_class: Type[ToolsBase]) -> Type[ToolsBase]:
    """
    Decorator to register a tool class in the registry
    
    Usage:
        @register_tool
        class MyTool(ToolsBase):
            # implementation
    
    Args:
        tool_class: The tool class to register
        
    Returns:
        The same tool class, unchanged (allows the decorator to be used without affecting the class)
    """
    ToolsRegistry.register(tool_class)
    return tool_class


if __name__ == "__main__":
    # No need to instantiate ToolsRegistry since it uses class methods
    print(ToolsRegistry.get_tools_parameters())
