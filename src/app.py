from pydantic import functional_serializers
import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.chatbot import Chatbot
from src.memory import ConversationMemory
from src.config import validate_config

app = FastAPI(title="Chatbot AI", version="1.0.0")

memory = ConversationMemory()
bot = None


def get_bot():
    global bot
    if bot is None:
        validate_config()
        bot = Chatbot()
    return bot


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class StatusResponse(BaseModel):
    status: str
    message: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Kirim pesan ke chatbot dan dapatkan balasan."""
    user_message = request.message.strip()
    if not user_message:
        return ChatResponse(reply="Pesan tidak boleh kosong.")

    try:
        current_bot = get_bot()
    except ValueError as e:
        return ChatResponse(reply=f"Error Konfigurasi: {e}")

    memory.add_message("user", user_message)
    response = current_bot.send_message(memory.get_history())
    memory.add_message("assistant", response)

    return ChatResponse(reply=response)


@app.post("/api/reset", response_model=StatusResponse)
async def reset():
    """Reset riwayat percakapan."""
    memory.clear()
    return StatusResponse(status="ok", message="Riwayat percakapan telah di-reset.")


@app.get("/api/history")
async def history():
    """Ambil riwayat percakapan saat ini."""
    return {"messages": memory.get_history()}


static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def serve_index():
    """Serve halaman utama."""
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)