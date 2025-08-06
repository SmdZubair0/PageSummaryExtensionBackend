import re

from pathlib import Path

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

from src.core.config import settings

class RetrieveFromVectorStore:

    def __init__(self, path : Path, embeddings):
        self.path = path
        self.embeddings = embeddings
        self._faiss = None

        self.prompt = PromptTemplate.from_template(
            "Extract any part of the context *AS IS* that is relevant to answer the question. "
            "If none of the context is relevant, return NO_OUTPUT.\n\nContext:\n{page_content}"
        )
        self.summarizer = ChatGroq(
            api_key = settings.groq_api_key,
            model = settings.summary_model_retrieval,
            temperature = 0.7,
            max_tokens = settings.generation_model_max_new_tokens,
        )
        self.llm_chain = self.prompt | self.summarizer

    def _load_index(self, deserialization = True):
        if self._faiss is None:
            self._faiss = FAISS.load_local(
                self.path,
                self.embeddings,
                allow_dangerous_deserialization = deserialization
            )
        return self._faiss

    def retrieve_from_Faiss(self,
                        k : int,
                        query : str,
                        deserialization : bool = True):
        try:
            docs = self._load_index(deserialization)
            
            compressor = LLMChainExtractor.from_llm(self.llm_chain)
            retriever = docs.as_retriever(search_kwargs = {"k": k})

            compression_retriever = ContextualCompressionRetriever(
                base_retriever = retriever,
                base_compressor = compressor
            )
            return compression_retriever.invoke(query)

        except FileNotFoundError:
            raise FileNotFoundError("please provide proper file path for faiss index...")
        except Exception as e:
            print(e)

    def retrieve_all_from_Faiss(self,
                                deserialization: bool = True):

        try:
            docs = FAISS.load_local(self.path, self.embeddings, allow_dangerous_deserialization = deserialization)
        except FileNotFoundError:
            raise FileNotFoundError("please provide proper file path for faiss index...")
        except Exception as e:
            print(e)

        return list(docs.docstore._dict.values())



def chunk_text(text, max_tokens = 1024, approx_chars_per_token = 4):
    max_chars = max_tokens * approx_chars_per_token
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + max_chars
        if end < text_len:
            space_pos = text.rfind(' ', start, end)
            if space_pos != -1 and space_pos > start:
                end = space_pos
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start = end
    return chunks

def clean_output(response_text : str) -> str:
    if response_text.strip().startswith("Here are the relevant sentences"):
        lines = response_text.strip().split("\n")[1:]
        cleaned_lines = [
            re.sub(r'^[*•\-]\s*"?([^"]+)"?', r'\1', line).strip()
            for line in lines if line.strip()
        ]
        response_text = "\n".join(cleaned_lines)

    return response_text