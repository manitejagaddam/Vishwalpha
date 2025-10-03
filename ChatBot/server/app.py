from fastapi import FastAPI
from pydantic import BaseModel
# from embeddings import get_embedding
# from qdrant_client import search_similar
from llm_client import generate_response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str


origins = [
    "http://localhost:5173",  # frontend URL
    "http://127.0.0.1:5173",
    # add any other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],    # allow all methods (GET, POST, etc.)
    allow_headers=["*"],    # allow all headers
)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    print("Server started")
    # 1. Convert user query to embedding
    # vector = get_embedding(req.message)
    
    # 2. Search Qdrant for context
    # context = search_similar(vector)
    
    # 3. Generate response with LLM
    answer = generate_response(req.message)
    print("answer : " , answer)
    
    return {"answer": answer}
