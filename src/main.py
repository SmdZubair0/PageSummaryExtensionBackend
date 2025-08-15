from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.DataLoader import app as dataloader_router
from src.api.TextSummarizer import app as summarizer_router
from src.api.Query import app as query_router

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Backend is running"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

app.include_router(summarizer_router, prefix="/summarize")
app.include_router(dataloader_router, prefix="/load")
app.include_router(query_router, prefix="/query")
