from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field

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