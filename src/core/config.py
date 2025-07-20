from pydantic_settings import BaseSettings
from pathlib import Path

class APISettings(BaseSettings):
    # CORS settings
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    # Dataloader settings
    text_splitter_chunk_size: int = 1000
    text_splitter_chunk_overlap: int = 100
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_location: str = str(Path("src/resources/faiss_index").resolve())

    # TextSummarization settings
    summary_model: str = "sshleifer/distilbart-cnn-12-6"
    summary_model_task: str = "summarization"
    summary_model_max_len: int = 1024
    summary_model_min_len: int = 512

    # Query settings
    query_model: str = "google/flan-t5-base"
    

    class Config:
        env_file = ".env"

settings = APISettings()