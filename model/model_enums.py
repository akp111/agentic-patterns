from enum import Enum

class RoleType(Enum):
    System: str  = "system"
    User: str = "user"
    Assistant: str = "assistant"
    Tool: str = "user"

class ProviderType(Enum):
    Groq: str = "groq"


class ModelType(Enum):
    Llama3_3_70B_Versatile: str = "llama-3.3-70b-versatile"