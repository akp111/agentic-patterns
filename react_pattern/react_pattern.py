from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from model.model_enums import RoleType, ProviderType, ModelType
from tools.tools_registry import ToolsRegistry
from config.env_manager import EnvManager
from model.model_factory import ModelFactory
import json
import re

@dataclass
class ReactPattern:
    user_prompt: str
    api_key: str
    user_history: List[Dict[str, str]] = field(default_factory=list)
    agent_history: List[Dict[str, str]] = field(default_factory=list)
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    available_tools: Dict[str, str] = field(default_factory=dict)
    verbose: bool = False
    env_manager: EnvManager = EnvManager()
    model: ModelFactory = None
    max_iterations: int = 5
    
    def __post_init__(self):
        list_of_tools = ToolsRegistry.list_available_tools()
        for tool in list_of_tools:
            tool_parameters = ToolsRegistry.get_tool_class(tool).get_tool_parameters()
            self.available_tools[tool] = tool_parameters
        self.model = ModelFactory(
            api_key=self.api_key,
            provider=ProviderType.Groq,
            model_name=ModelType.Llama3_3_70B_Versatile,
            verbose=self.verbose
        )
        self.conversation_history = self.construct_prompt()
    
    def construct_prompt(self):
        system_prompt = {
            "role": RoleType.System.value,
            "content": """You are a helpful assistant that can use tools to answer user queries. You operate by running a loop with the following steps: Thought, Act, Observation. 
You have access to the following tools:

"""
        }
        for tool_name, tool_params in self.available_tools.items():
            system_prompt["content"] += f"Tool: {tool_name}\n"
            system_prompt["content"] += f"Description: {tool_params.get('description', 'No description provided')}\n"
            system_prompt["content"] += f"Parameters: {json.dumps(tool_params.get('parameters', {}), indent=2)}\n\n"
        
        system_prompt["content"] += """
        
Pay special attention to the type of the parameters.
To use a tool, respond with:
```json
{
  "tool": "ToolName",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

Example session:
<question>Whats the weather at Bangalore?</question>
<thought>I need to use the weather tool to get the weather of Bangalore</thought>
```json
{
  "tool": "WeatherTool",
  "parameters": {
    "location": "Bangalore"
  }
}
```
You will get a response from the tool. You will then need to observe the response and think about what to do next.
<observation>40</observation>

You then output:

<response>It is 40 degrees in Bangalore</response>



If you need to use multiple tools, use them one at a time. Wait for the result of one tool before using another.
If you can answer the user's query without using tools, just respond normally.
"""
        conversation = [system_prompt]
        
        for i in range(len(self.user_history)):
            conversation.append({"role": RoleType.User.value, "content": self.user_history[i]["content"]})
            if i < len(self.agent_history):
                conversation.append({"role": RoleType.Assistant.value, "content": self.agent_history[i]["content"]})
        
        conversation.append({"role": RoleType.User.value, "content": f"<question>{self.user_prompt}</question>"})
        
        return conversation

    def parse_tags(self, response: str, tag: str) -> Optional[str]:
        """
        Parse the response to extract tags
        
        Args:
            response: The response from the model
            
        Returns:
            The parsed tag or None if not found
        """
        tag_pattern = fr'<({tag})>'
        tag_matches = re.findall(tag_pattern, response)
        
        if tag_matches:
            return tag_matches[0]
        
        return None
    
    def parse_tool_call(self, response: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Parse the response to extract tool calls
        
        Args:
            response: The response from the model
            
        Returns:
            A tuple of (tool_name, parameters) or (None, None) if no tool call found
        """
        json_pattern = r'```json\n(.*?)\n```'
        json_matches = re.findall(json_pattern, response, re.DOTALL)
        
        if not json_matches:
            json_pattern = r'```\n(.*?)\n```'
            json_matches = re.findall(json_pattern, response, re.DOTALL)
            
        if not json_matches:
            json_pattern = r'{[\s\S]*?"tool"[\s\S]*?}'
            json_matches = re.findall(json_pattern, response, re.DOTALL)
        
        for json_str in json_matches:
            try:
                tool_call = json.loads(json_str)
                if "tool" in tool_call and "parameters" in tool_call:
                    return tool_call["tool"], tool_call["parameters"]
            except json.JSONDecodeError:
                continue
        
        return None, None
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        Execute a tool with the given parameters
        
        Args:
            tool_name: The name of the tool to execute
            parameters: The parameters for the tool
            
        Returns:
            The result of the tool execution as a string
        """
        if tool_name not in ToolsRegistry.list_available_tools():
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            tool_instance = ToolsRegistry.create_tool(tool_name)
            result = tool_instance.run(**parameters)
            return f"Tool: {tool_name}\nResult: {result}"
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def run(self):
        
        iteration = 0
        final_response = ""
        while(iteration < self.max_iterations):
            response = self.model.generate(self.conversation_history, RoleType.Assistant)
            if self.verbose:
                print(f"\nIteration {iteration + 1} response:\n{response}")
            

            if "<response>" in response:
                parsed_response = self.parse_tags(response, "response")
                final_response = parsed_response.strip() if parsed_response else ""
            
            
            tool_name, parameters = self.parse_tool_call(response)
            
            if tool_name:
                tool_result = self.execute_tool(tool_name, parameters)
                
                self.conversation_history.append({
                    "role": RoleType.Assistant.value,
                    "content": response
                })
                
                observation = f"<observation>{tool_result}</observation>"
                self.conversation_history.append({
                    "role": RoleType.User.value,
                    "content": observation
                })
                
                iteration += 1
            else:
                # No tool call found, treat as final response
                final_response = response
                break
        
        if not final_response and iteration == self.max_iterations:
            self.conversation_history.append({
                "role": RoleType.User.value, 
                "content": "You've used up all your tool calls. Please provide your final answer based on the information collected."
            })
            
            response = self.model.generate(self.conversation_history, RoleType.Assistant)
            
            response_matches = self.parse_tags(response, "response")
            if response_matches:
                final_response = response_matches[0].strip()
            else:
                final_response = response
        
        self.agent_history.append({"content": final_response})
        
        return final_response




