from ..LLMInterface import LLMInterface
from ..LLMEnums import COHEREnums, DocumentTypeEnum
import logging
import cohere
class CohereProvider(LLMInterface):
    def __init__(self, api_key: str,
                default_input_max_characters: int = 1000,
                default_output_max_tokens:int = 1000,
                default_temperature:float = 0.9):
        
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generating_model_id = None
        self.embedding_model_id  = None
        self.embedding_model_size = None
        self.client = cohere.ClientV2(api_key=self.api_key) 

        self.logger = logging.getLogger(__name__)
    

    def set_generating_model(self,model_id:str):
        self.generating_model_id = model_id

    def set_embedding_model(self,model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_model_size = embedding_size

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
            self.construct_prompt(prompt=prompt,role=COHEREnums.USER.value)
        )

        response = self.client.chat(
            model= self.generating_model_id,
            messages= chat_history,
            max_tokens= max_output_tokens,
            temperature= temperature
        )

        if not response  or len(response.message.content[0].text) == 0 or  not response.message.content[0].text:

            self.logger.error("Error while generating text with OpenAI")
            return None
        return response.message.content[0].text

    def embed_text(self, text: str, document_type: str = DocumentTypeEnum.QUERY.value):
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was not set")
            return None       
            
        self.logger.info(f"Embedding text with model_id: {self.embedding_model_id}, input_type: {document_type}")
        
        # 1. Map internal DocumentTypeEnum to valid Cohere v3 input_types
        cohere_input_type = "search_query"
        if document_type == DocumentTypeEnum.DOCUMENT.value:
            cohere_input_type = "search_document"

        try:
            # 2. Use 'texts' with a flat list of strings and pass the mapped input_type
            response = self.client.embed(
                texts=[self.process_text(text)],
                model=self.embedding_model_id,
                input_type=cohere_input_type,
                embedding_types=["float"] # Explicitly specify to return float arrays
            )
        except Exception as e:
            self.logger.error(f"Error while embedding text with CoHere: {e}")
            return None
        
        # 3. Access floats correctly (Cohere Python SDK V2 returns .float_)
        if not response or not response.embeddings or not response.embeddings.float_:
            self.logger.error("Error while embedding text with CoHere: empty response")
            return None
            
        return response.embeddings.float_[0]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": COHEREnums.USER.value,
            "content": [{"type": "text", "text": self.process_text(prompt)}]
        }
    
    def construct_embed_text(self,text:str):
        return [{
            "content":{"type": "text", "text": text}
        }]