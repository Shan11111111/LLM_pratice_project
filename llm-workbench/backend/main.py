from fastapi import FastAPI
from routers import ingest, chat, summarize

app = FastAPI(title="LLM Multimodal RAG")

app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(summarize.router, prefix="/summarize", tags=["summarize"])
