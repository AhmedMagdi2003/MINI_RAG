from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CohereProvider
from helpers.config import Settings
from .providers.GeminiProvider import GeminiProvider
class LLMProviderFactory:
    def __init__(self, config: Settings):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            openai_provider =  OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )
            openai_provider.set_embedding_model(
                model_id=self.config.EMBEDDING_MODEL_ID,
                embedding_size=int(self.config.EMBEDDING_MODEL_SIZE)
            )
            openai_provider.set_generating_model(
                model_id=self.config.GENERATION_MODEL_ID
            )
            return openai_provider
        if provider == LLMEnums.COHERE.value:
            cohere_provider = CohereProvider(
                api_key = self.config.CO_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

            cohere_provider.set_embedding_model(
                model_id=self.config.EMBEDDING_MODEL_ID,
                embedding_size=int(self.config.EMBEDDING_MODEL_SIZE)
            )

            return cohere_provider
        if provider == "GEMINI":
            # 1. Capture the provider in a variable
            gemini_provider = GeminiProvider(
                api_key=self.config.GEMINI_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )
            
            # 2. Set the embedding model and size
            gemini_provider.set_embedding_model(
                model_id=self.config.EMBEDDING_MODEL_ID,
                embedding_size=int(self.config.EMBEDDING_MODEL_SIZE)
            )
            
            # 3. Set the generation model
            gemini_provider.set_generating_model(
                model_id=self.config.GENERATION_MODEL_ID
            )

            # 4. Return the fully configured provider
            return gemini_provider
        return None