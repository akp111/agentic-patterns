from .tools_registry import register_tool
from dataclasses import dataclass
from typing import Dict, List
from .tools_base import ToolsBase
import requests
import json

@register_tool
@dataclass
class HackerNews(ToolsBase):
    """ Fetches news from hackernews

    """
    name: str = "HackerNews"
    top_news_url: str = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    def init_tool(self, **kwargs):
        pass
    
    def run(self, no_of_stories: int) -> Dict[str, str]:
        try:
            response = requests.get(self.top_news_url)
            response.raise_for_status()
            
            top_stories_ids = response.json()[: no_of_stories]
            
            top_stories: List[Dict[str, str]] = []
            for story_id in top_stories_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_res = requests.get(story_url)
                story_res.raise_for_status()
                story_info: Dict = story_res.json()
                
                top_stories.append({
                    'title': story_info.get("title", "No Title"),
                    'url': story_info.get("url", "https://google.com")
                })
        
            return json.dumps(top_stories)
                   
        except Exception as e:
            print(e)
            raise(e)
    
    @staticmethod
    def get_tool_parameters()-> Dict:
        return {
            "name":"Hacker News Tool",
            "description":"Gets the latest hacker news based on the number of news provided by the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "no_of_stories":{
                        "type":"int",
                        "description":"Number of stories you want to fetch"
                    }
                },
                "required":["no_of_stories"]
            }
        }