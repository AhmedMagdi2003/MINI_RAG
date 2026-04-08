from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Mini-RAG"
    APP_VERSION: str = "1.0.0"
    FILE_ALLOWED_EXTENSIONS: Union[List[str], str] = Field(default=["txt", "pdf", "docx"])
    FILE_MAX_SIZE: int = 10485760  # 10MB
    FILE_DEFAULT_CHUNK_SIZE: int = 1024
    POSTGRES_USERNAME: str ="postgres"
    POSTGRES_PASSWORD: str ="PASSWORD"
    POSTGRES_HOST: str ="localhost"
    POSTGRES_PORT: int =5432
    POSTGRES_MAIN_DATABASE: str ="minirag"
    GENERATION_BACKEND: Optional[str] = None
    EMBEDDING_BACKEND: Optional[str] = None
    GENERATION_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_SIZE: Optional[int] = None
    INPUT_DAFAULT_MAX_CHARACTERS: Optional[int] = None
    GENERATION_DAFAULT_MAX_TOKENS: Optional[int] = None
    GENERATION_DAFAULT_TEMPERATURE: Optional[float] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_URL: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    CO_API_KEY: Optional[str] = None
    VECTOR_DB_BACKEND: str = None
    VECTOR_DB_PATH: str = None
    VECTOR_DB_DISTANCE_METHOD: Optional[str] = None
    PRIMARY_LANG: str = 'en'
    DEFAULT_LANG: str = 'en'

    @property
    def MONGODB_URL(self) -> str:
        return f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"

    @field_validator("FILE_ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

def get_settings():
    return Settings()