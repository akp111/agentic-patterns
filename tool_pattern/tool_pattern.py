from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from tools import ToolsRegistry
from model import ModelFactory, RoleType, ProviderType, ModelType


@dataclass
class ToolsPattern:
    
    user_history: List[Dict[str, str]] = field(default_factory=list)
    agent_history: List[Dict[str, str]] = field(default_factory=list)
    tool_parameters: Dict[str, Any] = field(default_factory=dict)
    model: ModelFactory = None
    verbose: bool = False
    groq_api_key: str = None
    
    
    def __post_init__(self):
        self.model = ModelFactory(
            api_key= self.groq_api_key,
            provider=ProviderType.Groq, 
            model_name=ModelType.Llama3_3_70B_Versatile, 
            verbose=self.verbose
        )
        self.construct_tool_parameters()
        if self.verbose:
            print(self.tool_parameters)
    
    def construct_tool_parameters(self) -> Dict:
        for tool in ToolsRegistry.list_available_tools():
            tool_class_params = ToolsRegistry.get_tool_class(tool).get_tool_parameters()
            self.tool_parameters[tool] = tool_class_params
    
    def construct_prompt(self, user_query: str) -> List[Dict[str, str]]:
        """
        Construct the prompt for the model with user query and tool definitions
        
        Args:
            user_query: The user's query/question
            
        Returns:
            A list of messages for the model
        """
        # System prompt with tool definitions
        system_prompt = {
            "role": RoleType.System.value,
            "content": """You are a helpful assistant that can use tools to answer user queries. 
You have access to the following tools:

"""
        }
        
        # Add tool descriptions to system prompt
        for tool_name, tool_params in self.tool_parameters.items():
            system_prompt["content"] += f"Tool: {tool_name}\n"
            system_prompt["content"] += f"Description: {tool_params.get('description', 'No description provided')}\n"
            system_prompt["content"] += f"Parameters: {json.dumps(tool_params.get('parameters', {}), indent=2)}\n\n"
        
        # Add instructions on how to use tools
        system_prompt["content"] += """
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

If you need to use multiple tools, use them one at a time. Wait for the result of one tool before using another.
If you can answer the user's query without using tools, just respond normally.
"""
        
        # Construct conversation history
        conversation = [system_prompt]
        
        # Add conversation history
        for i in range(len(self.user_history)):
            conversation.append({"role": RoleType.User.value, "content": self.user_history[i]["content"]})
            if i < len(self.agent_history):
                conversation.append({"role": RoleType.Assistant.value, "content": self.agent_history[i]["content"]})
        
        # Add current query
        conversation.append({"role": RoleType.User.value, "content": user_query})
        
        return conversation
    
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
    
    def run(self, user_query: str, max_iterations: int = 5) -> str:
        """
        Run the tool pattern with the user query
        
        Args:
            user_query: The user's query/question
            max_iterations: Maximum number of iterations for tool use
            
        Returns:
            The final response from the assistant
        """
        self.user_history.append({"content": user_query})
        
        iteration = 0
        final_response = ""
        
        while iteration < max_iterations:
            # Construct prompt
            prompt = self.construct_prompt(user_query if iteration == 0 else "")
            
            # Generate response
            response = self.model.generate(prompt, RoleType.Assistant)
            
            if self.verbose:
                print(f"\nIteration {iteration + 1} response:\n{response}")
            
            # Parse tool calls
            tool_name, parameters = self.parse_tool_call(response)
            
            if tool_name:
                tool_result = self.execute_tool(tool_name, parameters)
                self.agent_history.append({"content": response})
                self.user_history.append({"content": tool_result})
                iteration += 1
            else:
                final_response = response
                self.agent_history.append({"content": response})
                break
        if not final_response and iteration == max_iterations:
            prompt = self.construct_prompt("Please provide your final answer based on the tool results.")
            final_response = self.model.generate(prompt, RoleType.Assistant)
            self.agent_history.append({"content": final_response})
        
        return final_response


if __name__ == "__main__":
    tools_pattern = ToolsPattern(verbose=True)
    response = tools_pattern.run("What's the weather like in Bangalore today?")
    print("\nFinal response:")
    print(response)





