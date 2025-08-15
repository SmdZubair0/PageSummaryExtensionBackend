from pathlib import Path
from pydantic_settings import BaseSettings

class APISettings(BaseSettings):
    # keys
    groq_api_key: str
    huggingface_api_key: str
    
    # CORS settings
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    # Dataloader settings
    text_splitter_chunk_size: int = 1000
    text_splitter_chunk_overlap: int = 100
    vector_store_location: str = str(Path("src/resources/faiss_index").resolve())

    # HuggingFaceEmbeddingModel
    embedding_model_url: str = "https://api-inference.huggingface.co/models/sentence-transformers/distilbert-base-nli-mean-tokens"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # TextSummarization settings
    summary_model: str = "llama3-70b-8192"
    summary_model_task: str = "summarization"
    summary_model_max_len: int = 1024
    summary_model_min_len: int = 512

    # Query settings
    query_model: str = "llama3-70b-8192"
    generation_model_max_new_tokens: int = 512

    # Retriver settings
    summary_model_retrieval: str = "llama3-70b-8192"
    summary_model_task_retrieval: str = "summarization"
    summary_model_max_new_tokens: int = 200
    

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"

settings = APISettings()
