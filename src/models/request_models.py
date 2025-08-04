from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Literal

class PageData(BaseModel):
    url: Annotated[
        str,
        Field(
            title = "Page URL",
            description = "URL of the page in which the API is open"
        )
    ]
    title: Annotated[
        Optional[str],
        Field(
            title = "Page Title",
            description = "Title of the page in which API is called"
        )
    ] = None
    text: Annotated[
        str,
        Field(
            title = "Page content",
            description = "Main content of the page"
        )
    ]
    timestamp: Annotated[
        Optional[str],
        Field(
            title = "Timestamp",
            description = "Time stamp for which the API is called"
        )
    ] = None

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class QueryModel(BaseModel):
    query: Annotated[
        str,
        Field(
            title = "Query",
            description = "Query passed by user as input"
        )
    ]
    chat_history: Annotated[
        List[ChatMessage],
        Field(
            title="Chat History",
            description="List of previous messages in the conversation. Each message must include a 'role' (either 'user' or 'assistant') and the 'content'."
        )
    ] = []
    timestamp: Annotated[
        Optional[str],
        Field(
            title = "Timestamp",
            description = "Time stamp for which the API is called"
        )
    ] = None