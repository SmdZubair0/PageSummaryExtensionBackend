from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class PageData(BaseModel):
    url : str = Field(
        title = "Page URL",
        description = "URL of the page in which the API is open",
        example = "https://example.com/article"
    )
    title : Optional[str] = Field(
        default = None,
        title = "Page Title",
        description = "Title of the page in which API is called",
        example = "Understanding Machine Learning"
    )
    text : str = Field(
        title = "Page content",
        description = "Main content of the page",
        example = "This article explains the basics of machine learning..."
    )
    timestamp : Optional[str] = Field(
        default = None,
        title = "Timestamp",
        description = "Time stamp for which the API is called",
        example = "2025-08-04T14:30:00Z"
    )

class ChatMessage(BaseModel):
    role : Literal["user", "assistant"] = Field(
        example = "user"
    )
    content : str = Field(
        example = "What is machine learning?"
    )

class QueryModel(BaseModel):
    query : str = Field(
        title = "Query",
        description = "Query passed by user as input",
        example = "Summarize this article"
    )
    chat_history : List[ChatMessage] = Field(
        default_factory = list,
        title = "Chat History",
        description = "List of previous messages in the conversation.",
        example = [
            {"role" : "user", "content" : "Explain AI"},
            {"role" : "assistant", "content" : "AI stands for Artificial Intelligence..."}
        ]
    )
    timestamp : Optional[str] = Field(
        default = None,
        title = "Timestamp",
        description = "Time stamp for which the API is called",
        example = "2025-08-04T14:35:00Z"
    )
