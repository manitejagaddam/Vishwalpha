# Placeholder for Groq GPT OSS 20B integration
# Assuming a Python SDK or REST API
# from groq_gpt_sdk import GPTClient
from groq import Groq

def generate_response(query: str, context: list):
    """
    query: user query
    context: list of relevant texts from Qdrant
    """
    prompt = "Answer the question using the following context:\n\n"
    prompt += "\n".join(context) + f"\n\nQuestion: {query}\nAnswer:"
    
    # Example pseudo-call to Groq GPT OSS 20B
    client = Groq(model="openai/gpt-oss-20b")
    response = client.chat(prompt)
    
    return response.text
