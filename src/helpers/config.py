from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Mini-RAG"
    APP_VERSION: str = "1.0.0"
    FILE_ALLOWED_EXTENSIONS: Union[List[str], str] = Field(default=["txt", "pdf", "docx"])
    FILE_MAX_SIZE: int = 10485760  # 10MB
    FILE_DEFAULT_CHUNK_SIZE: int = 1024
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mini_rag"

    @field_validator("FILE_ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

def get_settings():
    return Settings()