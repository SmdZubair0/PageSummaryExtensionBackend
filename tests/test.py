# import os

# from langchain_huggingface import HuggingFaceEmbeddings

# from src.utils.helpers import RetrieveFromVectorStore

# from transformers import pipeline

# # llm = HuggingFaceEndpoint(
# #     repo_id="tiiuae/falcon-rw-1b",
# #     task="text-generation"
# # )
# # llm = HuggingFaceEndpoint(
# #     repo_id="facebook/bart-large-cnn",
# #     task="summarization"
# # )
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# faiss_index = os.path.join(os.getcwd(), "faiss_index")
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# retriever = RetrieveFromVectorStore(faiss_index, embeddings)


# def chunk_text(text, max_chars=3000):
#     return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# docs = retriever.retrieve_all_from_Faiss()

# intermediate_summaries = []

# for doc in docs:
#     chunks = chunk_text(doc.page_content)
#     chunk_summaries = []

#     for chunk in chunks:
#         result = summarizer(chunk, max_length=1024, min_length=512, do_sample=False)
#         chunk_summaries.append(result[0]["summary_text"])

#     combined_doc_summary = " ".join(chunk_summaries)
#     intermediate_summaries.append(combined_doc_summary)

# # Optional: Final summary of all summaries
# combined_summary_text = " ".join(intermediate_summaries)

# # Chunk again to stay safe
# final_chunks = chunk_text(combined_summary_text)
# final_summary = []

# for chunk in final_chunks:
#     result = summarizer(chunk, max_length=1024, min_length=200, do_sample=False)
#     final_summary.append(result[0]["summary_text"])

# final_output = " ".join(final_summary)

# print(final_output)


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from src.utils.HuggingFaceEmbeddingModel import HuggingFaceAPIEmbeddings

# embeddings = HuggingFaceAPIEmbeddings()

# embeddings._embed("hello")


import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/distilbert-base-nli-mean-tokens"
headers = {"Authorization": "Bearer "}

resp = requests.post(API_URL, headers=headers, json={"inputs": "Hello world"})
print(resp.status_code, resp.text)
