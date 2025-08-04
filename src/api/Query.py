from fastapi import APIRouter, HTTPException

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline

from src.utils.helpers import RetrieveFromVectorStore, chunk_text
from src.core.config import settings
from src.models.request_models import QueryModel
from src.models.response_models import QueryResponse

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

app = APIRouter()

model_id = settings.query_model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

llm_pipeline = pipeline(
    "text2text-generation",
    model = model,
    tokenizer = tokenizer,
    max_new_tokens = settings.generation_model_max_new_tokens,
    do_sample = True
)
llm = HuggingFacePipeline(pipeline = llm_pipeline)

embeddings = HuggingFaceEmbeddings(model_name = settings.embedding_model)

retriever = RetrieveFromVectorStore(
    settings.vector_store_location,
    embeddings = embeddings
)

system_prompt = SystemMessage(
    content="You are a helpful assistant. Use the context below to answer the question accurately."
)

@app.post("/", response_model = QueryResponse)
def ask_query(data: QueryModel):
    try:
        context_docs = retriever.retrieve_from_Faiss(
            k = 5,
            query = data.query
        )

        context_text = "\n".join([doc.page_content for doc in context_docs])

        messages = [system_prompt]

        if data.chat_history:
            for msg in data.chat_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content = msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content = msg.content))

        messages.append(
            HumanMessage(f"""
                You are a precise extraction engine.
                Extract any sentence(s) from the context *AS IS* that directly help answer the question below. 
                Return NO_OUTPUT if nothing in the context is relevant.
                Do NOT paraphrase or summarize.
                Context:
                {context_text}
                Question:
                {data.query}
            """)
        )

        response_raw = llm.invoke(messages)

        if isinstance(response_raw, str):
            response_text = response_raw
        elif isinstance(response_raw, list) and isinstance(response_raw[0], dict) and 'generated_text' in response_raw[0]:
            response_text = response_raw[0]['generated_text']
        else:
            response_text = str(response_raw)

        if response_text.strip() == "No_OUTPUT":
            response_text = "Couldn’t match the query to the content. Could you pass a more appropiate query please..."

        updated_history = data.chat_history + [
            {"role": "user", "content": data.query},
            {"role": "assistant", "content": response_text.strip()}
        ]

        return {
            "status": "success",
            "result": response_text.strip(),
            "chat_history": updated_history
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )