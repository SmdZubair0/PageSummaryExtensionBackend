from typing import Optional, Annotated
from pydantic import BaseModel, Field

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