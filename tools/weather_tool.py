from tools.tools_base import ToolsBase
from dataclasses import dataclass
from typing import Any, Optional, Dict
from requests import request
from .tools_registry import register_tool
from config.env_manager import EnvManager

@register_tool
@dataclass
class WeatherTool(ToolsBase):
    
    name: str = "Weather Tool"
    tool: Any = None
    base_url: str = "https://api.weatherapi.com/v1/current.json"
    api_key: Optional[str] = None
    
    def init_tool(self, **kwargs):
        """
        Initialize the weather tool
        This method is called automatically by the base class's __post_init__
        """
        # Initialize the EnvManager if not already initialized
        env_manager = EnvManager()
        
        # Get the API key from environment variables
        self.api_key = env_manager.get_weather_api_key(raise_error=True)
            
        self.base_url = f"{self.base_url}?key={self.api_key}"
    
    def run(self, location: str) -> Optional[float]:
        """
        Get the current temperature for a location
        
        Args:
            location (str): The location to get weather data for (city name, zip code, etc.)
            
        Returns:
            float or None: The current temperature in Celsius, or None if the request failed
        """
        
        url = f"{self.base_url}&q={location}"
        response = request("GET", url)
        if response.status_code == 200:
            data = response.json()
            return data.get("current", {}).get("temp_c", None)
        else:
            return None
    
    @staticmethod
    def get_tool_parameters() -> Dict:
        return {
            "name": "Weather Tool",
             "description": "Gets the current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to get weather data for (city name, zip code, etc.)"
                        }
                    },
                    "required": ["location"]
                }
        }
