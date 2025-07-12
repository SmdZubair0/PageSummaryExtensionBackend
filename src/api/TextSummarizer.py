import os
from fastapi import APIRouter, HTTPException

from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings

from src.core.config import settings
from src.models.response_models import TextSummarizerResponse
from src.utils.helpers import RetrieveFromVectorStore, chunk_text

app = APIRouter()

summarizer = pipeline(
    settings.summary_model_task,
    model = settings.summary_model
)

faiss_index = os.path.join(os.getcwd(), settings.vector_store_location)
embeddings = HuggingFaceEmbeddings(model_name = settings.embedding_model)
retriever = RetrieveFromVectorStore(faiss_index, embeddings)

@app.get("/", response_model = TextSummarizerResponse)
def summarize():
    try:
        docs = retriever.retrieve_all_from_Faiss()
        
        intermediate_summaries = []

        for doc in docs:
            chunks = chunk_text(doc.page_content)
            chunk_summaries = []

            for chunk in chunks:
                result = summarizer(
                    chunk,
                    max_length = settings.summary_model_max_len,
                    min_length = settings.summary_model_min_len,
                    do_sample=False
                )
                chunk_summaries.append(result[0]["summary_text"])

            combined_doc_summary = " ".join(chunk_summaries)
            intermediate_summaries.append(combined_doc_summary)

        combined_summary_text = " ".join(intermediate_summaries)

        final_chunks = chunk_text(combined_summary_text)
        final_summary = []

        for chunk in final_chunks:
            result = result = summarizer(
                chunk,
                max_length = settings.summary_model_max_len,
                min_length = settings.summary_model_min_len,
                do_sample=False
            )
            final_summary.append(result[0]["summary_text"])

        final_output = " ".join(final_summary)

        return {
            "status": "success",
            "summary": final_output
        }
    
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )