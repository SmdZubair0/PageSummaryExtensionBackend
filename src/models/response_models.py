from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, List, Dict
from src.models.request_models import ChatMessage

class DataloaderResponse(BaseModel):
    status: Annotated[
        str,
        Field(
            title = "Status",
            description = "Status of the API call"
        )
    ]
    timestamp: Annotated[
        datetime,
        Field(
            title = "Timestamp",
            description = "Timestamp of API call"
        )
    ]
    chunks: Annotated[
        int,
        Field(
            title = "No. of Chunks",
            description = "Number of chunks created from data"
        )
    ]

class TextSummarizerResponse(BaseModel):
    status: Annotated[
        str,
        Field(
            title = "Status",
            description = "Status of the API call"
        )
    ]
    summary: Annotated[
        str,
        Field(
            title = "Summary",
            description = "Summary of given data"
        )
    ]

class QueryResponse(BaseModel):
    status: Annotated[
        str,
        Field(
            title = "Status",
            description = "Status of the API call"
        )
    ]
    result: Annotated[
        str,
        Field(
            title = "Result",
            description = "Result of the query given by user"
        )
    ]
    chat_history: Annotated[
        List[ChatMessage],
        Field(
            title="Chat History",
            description="List of previous messages in the conversation. Each message must include a 'role' (either 'user' or 'assistant') and the 'content'."
        )
    ]