from fastapi import APIRouter, HTTPException

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.core.config import settings
from src.models.request_models import QueryModel
from src.models.response_models import QueryResponse
from src.utils.helpers import RetrieveFromVectorStore, clean_output
from src.utils.HuggingFaceEmbeddingModel import HuggingFaceAPIEmbeddings

app = APIRouter()

llm = ChatGroq(
    api_key = settings.groq_api_key,
    model = settings.query_model,
    temperature = 0.7,
    max_tokens = settings.generation_model_max_new_tokens
)

embeddings = HuggingFaceAPIEmbeddings()


system_prompt = SystemMessage(
    content="You are a helpful assistant. Use the context below to answer the question accurately."
)

@app.post("/{session_id}", response_model = QueryResponse)
def ask_query(data: QueryModel):

    storage_location = f"{session_id}_{uuid.uuid4().hex}_{settings.vector_store_location}"

    retriever = RetrieveFromVectorStore(
        storage_location,
        embeddings = embeddings
    )
    try:
        context_docs = retriever.retrieve_from_Faiss(
            k = 5,
            query = data.query
        )

        context_text = "\n".join([doc.page_content for doc in context_docs])

        if not context_docs:
            return {
                "status": "success",
                "result": "No relevant context found for the given query.",
                "chat_history": data.chat_history
            }
        
        context_text = context_text[:4000]

        messages = [system_prompt]

        if data.chat_history:
            for msg in data.chat_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content = msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content = msg.content))

        messages.append(
            HumanMessage(content=f"""
                You are a precise extraction engine.
                Analyze the context passed below and answer the query given below.
                Return NO_OUTPUT if nothing in the context is relevant.
                Context:
                {context_text}
                Question:
                {data.query}
            """)
        )

        response_raw = llm.invoke(messages)


        if isinstance(response_raw, AIMessage):
            response_text = response_raw.content
        elif isinstance(response_raw, str):
            response_text = response_raw
        elif isinstance(response_raw, list) and isinstance(response_raw[0], dict) and 'generated_text' in response_raw[0]:
            response_text = response_raw[0]['generated_text']
        else:
            response_text = str(response_raw)

        response_text = clean_output(response_text)

        if response_text.strip() == "NO_OUTPUT":
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