from enum import Enum

class LLMEnums(Enum):

    OPENAI = 'OPENAI'
    COHERE = 'COHERE'
    GEMINI = 'GEMINI'

class OpenAIEnums(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = "assistant"
class COHEREnums(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = "assistant"

class GeminiEnums(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = "assistant"
class DocumentTypeEnum(Enum):
    DOCUMENT = 'search_document'
    QUERY = "search_query"