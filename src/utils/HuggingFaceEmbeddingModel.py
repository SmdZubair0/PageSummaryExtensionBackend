import requests

from langchain.embeddings.base import Embeddings

from src.core.config import settings

class HuggingFaceAPIEmbeddings(Embeddings):
    def __init__(self):
        self.api_token = settings.huggingface_api_key
        self.model_url = settings.embedding_model_url
        self.headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        response = requests.post(self.model_url, headers=self.headers, json={"inputs": text})
        return response.json()[0]
