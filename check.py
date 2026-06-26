import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API KEY FOUND:", api_key is not None)