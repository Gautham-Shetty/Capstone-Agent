import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)


def get_embeddings(text:str):
    embeddings = genai.embed_content(
        model="text-embedding-004",
        content=text
    )
    return embeddings["embedding"]


