from fastapi import FastAPI
from pydantic import BaseModel
from embeddings import get_embedding
from qdrant_client import search_similar
from llm_client import generate_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1. Convert user query to embedding
    vector = get_embedding(req.message)
    
    # 2. Search Qdrant for context
    context = search_similar(vector)
    
    # 3. Generate response with LLM
    answer = generate_response(req.message, context)
    
    return {"answer": answer}
