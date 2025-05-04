from . import model_base
from . import model_enums
from groq import Groq as GroqClient
import logging
from typing import Optional

class GroqModel(model_base.ModelBase):
    """
    Groq model implementation that inherits from ModelBase.
    """
    
    def init_model(self) -> bool:
        """
        Initialize the Groq client with the API key.
        :return: True if initialization was successful, False otherwise
        """
        try:
            self.model = GroqClient(api_key=self.api_key)
            return True
        except Exception as e:
            logging.error(f"Failed to initialize Groq client: {str(e)}")
            return False
    
    def generate(self, prompt: model_base.PromptType, role: Optional[model_enums.RoleType] = None) -> Optional[str]:
        """
        Generate a response using the Groq API.
        
        :param prompt: Text prompt or list of message objects to send to the model.
                     If a string is provided, it will be wrapped in a message object with the specified role.
                     If a list is provided, it should contain properly formatted message objects.
        :param role: Role type for the request (used only if prompt is a string)
        :return: Generated text response or None if there's an error
        """
        if not prompt:
            logging.warning("Empty prompt provided to generate method")
            return None
            
        if self.verbose:
            print(f"Generating response for prompt: {prompt}")
            
        try:
            # Handle both string prompts and message arrays
            if isinstance(prompt, str):
                if role is None:
                    role = model_enums.RoleType.User
                messages = [{"role": role.value, "content": prompt}]
            else:
                messages = prompt
                
            response = self.model.chat.completions.create(
                messages=messages,
                model=self.model_name.value
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during Groq API call: {str(e)}")
            return f"Error: {str(e)}"