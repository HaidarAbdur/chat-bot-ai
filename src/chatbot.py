# pyrefly: ignore [missing-import]
from Gemini import gemini
from src.config import API_KEY, MODEL_NAME, SYSTEM_PROMPT

class Chatbot:
    def __init__(self):
        self.client = gemini(api_key=API_KEY)

    def send_message(self, history: list) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"