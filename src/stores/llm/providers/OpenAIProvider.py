from ..LLMinterface import LLMinterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMinterface):

    def __init__(self, api_key: str, api_url: str = None,  # type: ignore
                default_input_max_characters: int = 1000,
                default_output_max_tokens:int = 1000,
                default_temperature:float = 0.3):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generating_model_id = None
        self.embedding_model_id  = None
        self.embedding_model_size = None

        self.client = OpenAI(
            api_key  = self.api_key,
            base_url = self.api_url
        )

        self.logger = logging.getLogger(__name__)
    

    def set_generating_model(self,model_id:str):
        self.generating_model_id = model_id

    def set_embedding_model(self,model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_model_size = embedding_size

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": OpenAIEnums.USER.value,
            "content": [{"type": "text", "text": self.process_text(prompt)}]
        }

    def process_text(self,text):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str,chat_history:list = None, temperature: float = None, max_output_tokens: int = None ):
        
        if chat_history is None:
            chat_history=[]
        if not self.client:
            self.logger.error("OpenAI client was not set")

        if not self.generating_model_id:
            self.logger.error("Generation model for OpenAI want not set")
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature = self.default_temperature if temperature is None else temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt,role=OpenAIEnums.USER.value)
        )

        response = self.client.responses.create(
            model= self.generating_model_id,
            input= chat_history,
            max_output_tokens= max_output_tokens,
            temperature= temperature
        )

        if not response  or len(response.output[0]) == 0 or  not response.output[0].content[0]:

            self.logger.error("Error while generating text with OpenAI")
            return None
        return response.output[0].content[0].text

    def embed_text(self, text: str, documnet_type: str= None):
        
        if not self.client:
            self.logger.error("OpenAI client was not set")

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI want not set")
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id, # pyright: ignore[reportArgumentType]
            input = text
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Erro while rembedding text with OpennAI")