import requests

from langchain.embeddings.base import Embeddings

from src.core.config import settings

class HuggingFaceAPIEmbeddings(Embeddings):
    def __init__(self):
        self.api_token = settings.huggingface_api_key
        self.model_url = settings.embedding_model_url
        self.headers = {
            "Authorization": f"Bearer {settings.huggingface_api_key}",
            "x-use-cache": "false"
        }

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        response = requests.post(
            self.model_url,  
            headers=self.headers,
            json ={"inputs": text},
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"HuggingFace API request failed [{response.status_code}]: {response.text}"
            )

        data = response.json()

        if not isinstance(data, list) or not all(isinstance(x, (float, int)) or isinstance(x, list) for x in data):
            raise ValueError(f"Unexpected response format: {data}")

        if isinstance(data[0], list):
            return [sum(col) / len(col) for col in zip(*data)]
        return data
