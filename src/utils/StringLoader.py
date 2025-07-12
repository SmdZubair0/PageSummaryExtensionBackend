from typing import Iterator
from langchain.schema import Document

class StringLoader:
    def __init__(self, text: str):
        self.text = text

    def load(self) -> list[Document]:
        return [Document(page_content=self.text)]

    def lazy_load(self) -> Iterator[Document]:
        yield Document(page_content=self.text)
