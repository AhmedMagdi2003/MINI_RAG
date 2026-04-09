from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum,GeminiEnums
import google.generativeai as genai
import logging
import time
class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str,
                 default_input_max_characters: int = 10000,
                 default_output_max_tokens: int = 1000,
                 default_temperature: float = 0.3):
        
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generating_model_id = None
        self.embedding_model_id  = None
        self.embedding_model_size = None

        # Configure the Gemini client globally
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.enums = GeminiEnums
        self.logger = logging.getLogger(__name__)

    def set_generating_model(self, model_id: str):
        self.generating_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_model_size = embedding_size

    def process_text(self, text):
        return text[:self.default_input_max_characters].strip()

    def construct_prompt(self, prompt: str, role: str):
        # We map 'system' or 'user' to 'user', and 'assistant' to 'model'.
        gemini_role = "model" if role == "assistant" else "user"
        return {
            "role": gemini_role,
            "parts": [prompt]
        }

    def generate_text(self, prompt: str, chat_history: list = None, temperature: float = None, max_output_tokens: int = None):
        if chat_history is None:
            chat_history = []
            
        if not self.generating_model_id:
            self.logger.error("Generation model for Gemini was not set")
            return None
        
        max_tokens = max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temp = self.default_temperature if temperature is None else temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role="user")
        )

        # Gemini API crashes if there are consecutive 'user' roles in chat history.
        # This loop safely merges system prompts and user prompts together.
        merged_contents = []
        for msg in chat_history:
            if merged_contents and merged_contents[-1]["role"] == msg["role"]:
                merged_contents[-1]["parts"][0] += f"\n\n{msg['parts'][0]}"
            else:
                merged_contents.append(msg)

        try:
            model = genai.GenerativeModel(
                model_name=self.generating_model_id,
                generation_config=genai.types.GenerationConfig(
                    temperature=temp,
                    max_output_tokens=max_tokens,
                )
            )
            response = model.generate_content(merged_contents)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error while generating text with Gemini: {str(e)}")
            return None

    def embed_text(self, text: str, document_type: str = None):
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        # Gemini optimizations for embeddings
        task_type = "RETRIEVAL_DOCUMENT" if document_type == DocumentTypeEnum.DOCUMENT.value else "RETRIEVAL_QUERY"
        
        try:
            response = genai.embed_content(
                model=self.embedding_model_id,
                content=self.process_text(text),
                task_type=task_type,
                output_dimensionality=self.embedding_model_size
            )
            
            if response and 'embedding' in response:
                return response['embedding']
            return None
            
        except Exception as e:
            self.logger.error(f"Error while embedding text with Gemini: {str(e)}")
            return None

    def embed_batch(self, texts: list, document_type: str = None):
        if not self.embedding_model_id:
            return None
            
        task_type = "RETRIEVAL_DOCUMENT" if document_type == DocumentTypeEnum.DOCUMENT.value else "RETRIEVAL_QUERY"
        processed_texts = [self.process_text(text) for text in texts]
        
        all_embeddings = []
        # Reduce batch size to 50 to safely stay under the 100-chunk limit
        batch_size = 50 
        
        for i in range(0, len(processed_texts), batch_size):
            batch = processed_texts[i:i+batch_size]
            
            # Retry logic: If we hit a 429, wait 60 seconds and try again
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = genai.embed_content(
                        model=self.embedding_model_id,
                        content=batch,
                        task_type=task_type,
                        output_dimensionality=self.embedding_model_size
                    )
                    all_embeddings.extend(response['embedding'])
                    break # Success! Break out of the retry loop
                    
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Quota exceeded" in error_msg:
                        self.logger.warning(f"Gemini API rate limit hit. Sleeping for 60 seconds... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(60) # Pause the application for 60 seconds
                        if attempt == max_retries - 1:
                            self.logger.error("Max retries reached. Failing batch.")
                            return None
                    else:
                        self.logger.error(f"Error while embedding batch with Gemini: {error_msg}")
                        return None
            
            # A tiny pause between successful batches just to be safe
            time.sleep(1)
            
        return all_embeddings