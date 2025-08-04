from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from src.models.request_models import ChatMessage

class DataloaderResponse(BaseModel):
    status : str = Field(
        title = "Status",
        description = "Status of the API call",
        example = "success"
    )
    timestamp : datetime = Field(
        title = "Timestamp",
        description = "Timestamp of API call",
        example = "2025-08-04T15:00:00Z"
    )
    chunks : int = Field(
        title = "No. of Chunks",
        description = "Number of chunks created from data",
        example = 5
    )

class TextSummarizerResponse(BaseModel):
    status : str = Field(
        title = "Status",
        description = "Status of the API call",
        example = "success"
    )
    summary : str = Field(
        title = "Summary",
        description = "Summary of given data",
        example = "This article discusses how AI is transforming modern education systems."
    )

class QueryResponse(BaseModel):
    status : str = Field(
        title = "Status",
        description = "Status of the API call",
        example = "success"
    )
    result : str = Field(
        title = "Result",
        description = "Result of the query given by user",
        example = "AI stands for Artificial Intelligence, which enables machines to mimic human intelligence."
    )
    chat_history : List[ChatMessage] = Field(
        title = "Chat History",
        description = "List of previous messages in the conversation. Each message must include a 'role' (either 'user' or 'assistant') and the 'content'.",
        example = [
            {"role" : "user", "content" : "What is AI?"},
            {"role" : "assistant", "content" : "AI stands for Artificial Intelligence..."}
        ]
    )
