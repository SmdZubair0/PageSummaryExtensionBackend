import logging

from src.core.config import settings
from src.models.request_models import PageData
from src.utils.StringLoader import StringLoader
from src.models.response_models import DataloaderResponse

from fastapi import APIRouter, HTTPException

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger()

app = APIRouter()

@app.post("/", response_model = DataloaderResponse)
def upload_data(data: PageData):

    try:
        loader = StringLoader(data.text)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.text_splitter_chunk_size,
            chunk_overlap = settings.text_splitter_chunk_overlap
        )
        chunks = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(model_name = settings.embedding_model)

        vectorstore = FAISS.from_documents(chunks, embeddings)

        vectorstore.save_local(settings.vector_store_location)

        return {
            "status": "success",
            "timestamp": data.timestamp,
            "chunks": len(chunks)
        }
    
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    