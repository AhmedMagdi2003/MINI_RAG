from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, api_url: str = None,  # type: ignore
                default_input_max_characters: int = 1000,
                default_output_max_tokens: int = 1000,
                default_temperature: float = 0.3):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generating_model_id = None
        self.embedding_model_id  = None
        self.embedding_model_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url if self.api_url or len(self.api_url)>0 else None
        )

        self.logger = logging.getLogger(__name__)

    def set_generating_model(self, model_id: str):
        self.generating_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_model_size = embedding_size

    def construct_prompt(self, prompt: str, role: str):
        # FIX: Use the actual role passed to the function, and format content properly
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

    def process_text(self, text):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = None, temperature: float = None, max_output_tokens: int = None):
        
        if chat_history is None:
            chat_history = []
            
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generating_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        
        max_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temp = self.default_temperature if temperature is None else temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        try:
            # FIX: Use the correct chat.completions endpoint and parameters
            response = self.client.chat.completions.create(
                model=self.generating_model_id,
                messages=chat_history,
                max_tokens=max_tokens,
                temperature=temp
            )
            
            # FIX: Parse the OpenAI response object correctly
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error while generating text with OpenAI: {str(e)}")
            return None

    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model_id,
                input=self.process_text(text)
            )
            
            # FIX: Actually return the embedding!
            if response and response.data and len(response.data) > 0:
                return response.data[0].embedding
            return None
            
        except Exception as e:
            self.logger.error(f"Error while embedding text with OpenAI: {str(e)}")
            return None