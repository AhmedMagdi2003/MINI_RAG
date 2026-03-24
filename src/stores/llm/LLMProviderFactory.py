from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CohereProvider
from helpers.config import Settings
class LLMProviderFactory:
    def __init__(self, config: Settings):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

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

        return None