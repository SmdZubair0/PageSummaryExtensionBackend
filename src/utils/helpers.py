from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate

from transformers import pipeline
from src.core.config import settings

from transformers import AutoTokenizer

class RetrieveFromVectorStore:

    def __init__(self, path : Path, embeddings):
        self.path = path
        self.embeddings = embeddings
        self._faiss = None

        self.summarizer_pipeline = pipeline(
            task = settings.summary_model_task,
            model = settings.summary_model,
            max_new_tokens = settings.summary_model_max_new_tokens,
            do_sample = False
        )

        self.prompt = PromptTemplate.from_template(
            "Extract any part of the context *AS IS* that is relevant to answer the question. "
            "If none of the context is relevant, return NO_OUTPUT.\n\nContext:\n{page_content}"
        )
        self.summarizer = HuggingFacePipeline(pipeline = self.summarizer_pipeline)
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



def chunk_text(text, max_tokens = 1024):
    tokenizer = AutoTokenizer.from_pretrained(settings.summary_model)
    tokens = tokenizer.encode(text, truncation=False)
    chunks = [tokens[i : i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]
