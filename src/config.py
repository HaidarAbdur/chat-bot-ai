import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

API_KEY = (
    os.getenv("GEMINI_API_KEY") 
    or os.getenv("gemini_api_key") 
    or os.getenv("API_KEY") 
    or os.getenv("api_key")
)

MODEL_NAME = (
    os.getenv("MODEL_NAME") 
    or os.getenv("model_name") 
    or "gemini-3.6-flash"
)

SYSTEM_PROMPT = (
    os.getenv("SYSTEM_PROMPT") 
    or os.getenv("system_prompt") 
    or "Kamu adalah asisten AI yang ramah, cerdas, dan sopan. Bantu user sebaik mungkin."
)

def validate_config():
    if not API_KEY:
        raise ValueError("API KEY tidak ditemukan di .env")
