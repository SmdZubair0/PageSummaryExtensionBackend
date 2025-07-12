from fastapi import FastAPI

from src.api.DataLoader import app as dataloader_router
from src.api.TextSummarizer import app as summarizer_router

app = FastAPI()

app.include_router(summarizer_router, prefix="/summarize")
app.include_router(dataloader_router, prefix="/load")
