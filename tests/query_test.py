from fastapi import APIRouter, HTTPException

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings

from extension.src.utils.helpers import RetrieveFromVectorStore
from extension.src.core.config import settings
from extension.src.models.request_models import QueryModel
from extension.src.models.response_models import QueryResponse

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

model_id = settings.query_model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

embeddings = HuggingFaceEmbeddings(model_name = settings.embedding_model)

retriever = RetrieveFromVectorStore(
    settings.vector_store_location,
    embeddings = embeddings
)

system_prompt = SystemMessage(
    content="You are a helpful assistant. Use the context below to answer the question accurately."
)

d = {
    "query" : "what are the types of testing?",
    "chat_history" : [],
    "timestamp" : None
}
data = QueryModel(**d)
def ask_query(data: QueryModel):
    try:
        context_docs = retriever.retrieve_from_Faiss(
            k=5,
            query=data.query
        )
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        print(context_text)

        messages = [system_prompt]

        if data.chat_history:
            for msg in data.chat_history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))

        messages.append(HumanMessage(content=f"Context:\n{context_text}\n\nQuestion:\n{data.query}"))

        print(messages)

        response_raw = llm.invoke(messages)

        if isinstance(response_raw, str):
            response_text = response_raw
        elif isinstance(response_raw, list) and isinstance(response_raw[0], dict) and 'generated_text' in response_raw[0]:
            response_text = response_raw[0]['generated_text']
        else:
            response_text = str(response_raw)

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

ask_query(data)