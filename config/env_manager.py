"""
Environment variable management for AI Agents project.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class EnvManager:
    """
    Manage environment variables for various tools in the AI Agents project.
    
    This class handles loading environment variables from .env files and provides
    a centralized way to access them across different tools.
    """
    
    _instance = None  
    _env_loaded = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EnvManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize the environment manager.
        
        Args:
            env_file: Optional path to a specific .env file. If None, will try to
                     locate .env files in standard locations.
        """
        if not EnvManager._env_loaded:
            self._load_environment(env_file)
            EnvManager._env_loaded = True
    
    def _load_environment(self, env_file: Optional[str] = None) -> None:
        """
        Load environment variables from .env files.
        
        Args:
            env_file: Optional path to a specific .env file
        """
        # If a specific env file is provided, load it
        if env_file and Path(env_file).exists():
            load_dotenv(env_file)
            return
            
        # Try to locate .env files in standard locations
        # Check project root
        root_env = Path(__file__).parent.parent / '.env'
        if root_env.exists():
            load_dotenv(root_env)
            return
            
        # Check example directory
        example_env = Path(__file__).parent.parent / 'example' / '.env'
        if example_env.exists():
            load_dotenv(example_env)
            return
            
        # Fallback to dotenv's default behavior (looking in current working directory)
        load_dotenv()
    
    @staticmethod
    def get_api_key(key_name: str, raise_error: bool = False, default: Any = None) -> Optional[str]:
        """
        Get an API key from environment variables.
        
        Args:
            key_name: Name of the environment variable containing the API key
            raise_error: Whether to raise an error if the key is not found
            default: Default value to return if the key is not found
            
        Returns:
            API key value or default if not found
            
        Raises:
            ValueError: If raise_error is True and the key is not found
        """
        api_key = os.getenv(key_name, default)
        if api_key is None and raise_error:
            raise ValueError(f"API key '{key_name}' is required but not found in environment variables.")
        return api_key
    
    @staticmethod
    def get_weather_api_key(raise_error: bool = True) -> Optional[str]:
        """
        Get the Weather API key.
        
        Args:
            raise_error: Whether to raise an error if the key is not found
            
        Returns:
            Weather API key
        """
        return EnvManager.get_api_key("WEATHER_API_KEY", raise_error)
    
    @staticmethod
    def get_groq_api_key(raise_error: bool = True) -> Optional[str]:
        """
        Get the Groq API key.
        
        Args:
            raise_error: Whether to raise an error if the key is not found
            
        Returns:
            Groq API key
        """
        return EnvManager.get_api_key("GROQ_API_KEY", raise_error)