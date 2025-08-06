import os
import asyncio

from fastapi import APIRouter, HTTPException

from langchain_groq import ChatGroq

from src.utils.helpers import *
from src.core.config import settings
from src.models.response_models import TextSummarizerResponse
from src.utils.HuggingFaceEmbeddingModel import HuggingFaceAPIEmbeddings

app = APIRouter()

llm = ChatGroq(
    api_key = settings.groq_api_key,
    model = settings.summary_model,
    temperature = 0.7,
    max_tokens = settings.generation_model_max_new_tokens,
)

faiss_index = os.path.join(os.getcwd(), settings.vector_store_location)
embeddings = HuggingFaceAPIEmbeddings()
retriever = RetrieveFromVectorStore(faiss_index, embeddings)

@app.get("/", response_model = TextSummarizerResponse)
async def summarize():
    try:
        docs = retriever.retrieve_all_from_Faiss()
        
        intermediate_summaries = []

        for doc in docs:

            summary = await llm.ainvoke(doc.page_content)
            intermediate_summaries.append(summary.content)

        combined_summary_text = " ".join(intermediate_summaries)

        final_chunks = chunk_text(combined_summary_text, 1000)
        final_summary = []

        for chunk in final_chunks:
            result = await  llm.ainvoke(chunk)
            final_summary.append(result.content)

        final_output = " ".join(final_summary)
        final_output = clean_output(final_output)

        return {
            "status": "success",
            "summary": final_output
        }
    
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )