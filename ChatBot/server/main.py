import os
from fastapi import FastAPI
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


load_dotenv()


api_key = os.getenv("GROQ_KEY")

client = Groq(api_key=api_key)


app = FastAPI()

class ChatResponse(BaseModel):
    answer : str
    
class ChatRequest(BaseModel):
    question : str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req : ChatRequest):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages= [{"role" : "user", "content" : "You are a Education Tutor Bot who gives answers considering all the edge cases and the indepth explanation"}]
    )
    
    output