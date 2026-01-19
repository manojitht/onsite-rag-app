import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CHROMA_DB_DIR: str = "data/chroma"
    UPLOAD_DIR: str = "data/uploads"
    AUDIT_LOG_PATH: str = "logs/audit.jsonl"
    # POLICY_PATH: str = "data/policies/policy_scholarship_and_program.txt"
    
    openai_model: str = "gpt-4o-mini"
    openai_embed_model: str = "text-embedding-3-large"
    
    chunk_size: int = 600
    chunk_overlap: int = 150
    TOP_K: int = 3
    
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()


os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

