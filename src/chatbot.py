# pyrefly: ignore [missing-import]
from google import genai
import chromadb
# pyrefly: ignore [missing-import]
from google.genai import types
from src.config import API_KEY, MODEL_NAME, SYSTEM_PROMPT

class Chatbot:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)

    def send_message(self, history: list) -> str:
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        try:
                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )
                return response.text
        except Exception as e:
            return f"Error:{e}"