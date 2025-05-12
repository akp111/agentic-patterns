from .tools_registry import register_tool
from dataclasses import dataclass
from .tools_base import ToolsBase
from duckduckgo_search import DDGS
@register_tool
@dataclass
class DuckDuckGoSearch(ToolsBase):
    """ DuckDuckGo Search Tool
    """
    name: str = "DuckDuckGo Search"
    
    def init_tool(self, **kwargs):
        self.ddgs = DDGS()
    
    def run(self, query: str, search_type: str = "text") -> str:
        print(query)
        if search_type == "text":
           results = self.ddgs.text(query, max_results=5)
           result_str = ""
           for idx, item in enumerate(results, 1):
               result_str += f"{idx}. {item.get('title', 'No Title')}: {item.get('body', 'No description')} - {item.get('href', 'No link')}\n\n"
           print(result_str)
           return result_str
        elif search_type == "images":
              results = self.ddgs.images(query, max_results=5)
              result_str = ""
              for idx, item in enumerate(results, 1):
                  result_str += f"{idx}. {item.get('title', 'No Title')}: {item.get('image', 'No image')} - {item.get('url', 'No link')}\n\n"
              return result_str
    
    @staticmethod
    def get_tool_parameters() -> dict:
        return {
            "name": "DuckDuckGo Search Tool",
            "description": "Searches DuckDuckGo for a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    },
                    "search_type": {
                        "type": "string",
                        "description": "Type of search (text or images)."
                    }
                },
                "required": ["query"]
            }
        }
