# Placeholder for Groq GPT OSS 20B integration
# Assuming a Python SDK or REST API
# from groq_gpt_sdk import GPTClient
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

def generate_response(query: str, context: list = []):
    """
    query: user query
    context: list of relevant texts from Qdrant
    """
    prompt = " Your Name is Alpha Bot Answer the question using the following context:\n\n"
    # prompt += "\n".join(context) + f"\n\nQuestion: {query}\nAnswer:"
    prompt += f"\n\nQuestion: {query}\nAnswer:"
    
    # Example pseudo-call to Groq GPT OSS 20B
    # client = Groq(model="openai/gpt-oss-20b")
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    # client = Groq()
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    
    return response.choices[0].message.content
