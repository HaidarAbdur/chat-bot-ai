# DESIGN — Chatbot AI (Python)

## 1. Ringkasan Arsitektur
Chatbot ini adalah aplikasi CLI Python yang:
1. Menerima input teks dari user di terminal.
2. Mengirim input tersebut (+ riwayat chat) ke API model AI (Anthropic Claude).
3. Menerima respons dan menampilkannya ke user.
4. Menyimpan riwayat percakapan di memori (list) agar konteks tetap nyambung.

```
User (terminal)
      │  input teks
      ▼
 main.py  ──────────────►  chatbot.py  ──────────► Anthropic API
      ▲                         │                        │
      │                         ▼                        │
      └──────── output teks ◄── memory.py  ◄──────────────┘
                              (riwayat chat)
```

## 2. Struktur Folder

```
chatbot-ai/
├── README.md
├── PRD.md
├── DESIGN.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py         # entry point, loop percakapan CLI
│   ├── chatbot.py       # logic komunikasi ke API model AI
│   ├── config.py        # load API key & konfigurasi dari .env
│   └── memory.py        # kelola riwayat percakapan (session/file)
└── tests/
    └── test_chatbot.py  # unit test dasar
```

## 3. Komponen & Tanggung Jawab

### `config.py`
- Membaca `.env` (pakai `python-dotenv`).
- Menyediakan konstanta seperti `API_KEY`, `MODEL_NAME`, `SYSTEM_PROMPT`.
- Validasi: kalau API key kosong, langsung beri pesan error yang jelas.

### `memory.py`
- Kelas `ConversationMemory` yang menyimpan list pesan (`{"role": "user"/"assistant", "content": "..."}`).
- Method: `add_message()`, `get_history()`, `clear()`, dan opsional `save_to_file()` / `load_from_file()`.
- Bisa membatasi jumlah pesan lama yang disimpan (supaya token tidak membengkak).

### `chatbot.py`
- Kelas `Chatbot` yang membungkus panggilan ke Anthropic API.
- Method utama: `send_message(user_input: str) -> str`.
- Bertanggung jawab menyusun `messages` (riwayat + pesan baru) dan memanggil API.
- Menangani error (timeout, rate limit, API key invalid) dengan try/except yang informatif.

### `main.py`
- Loop utama: baca input user → panggil `chatbot.send_message()` → cetak balasan.
- Menangani perintah khusus, misalnya `/exit` untuk keluar, `/reset` untuk menghapus memori.

## 4. Pilihan Teknologi
- **Bahasa**: Python 3.10+
- **Model AI**: Anthropic Claude via `anthropic` SDK resmi (model `claude-sonnet-5` sebagai default — cepat & murah untuk chatbot personal).
- **Env management**: `python-dotenv` untuk baca `.env`.
- **Testing**: `pytest` (opsional tapi disarankan).

## 5. Alur Data Contoh (Sequence)
1. User mengetik: `"Halo, siapa namamu?"`
2. `main.py` memanggil `memory.add_message("user", "Halo, siapa namamu?")`.
3. `chatbot.send_message()` mengambil seluruh riwayat dari `memory.get_history()`.
4. Riwayat + system prompt dikirim ke Anthropic API.
5. Respons diterima → disimpan lagi ke memory sebagai pesan `"assistant"`.
6. Respons ditampilkan ke user di terminal.

## 6. Contoh Kode Inti (`chatbot.py`)

```python
import anthropic
from src.config import API_KEY, MODEL_NAME, SYSTEM_PROMPT

class Chatbot:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=API_KEY)

    def send_message(self, history: list) -> str:
        response = self.client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history,
        )
        return response.content[0].text
```

## 7. Penanganan Error
- **API key kosong/salah** → tampilkan pesan jelas + hentikan program dengan rapi (jangan traceback mentah).
- **Koneksi gagal/timeout** → tangkap exception, beri pesan "Gagal terhubung, coba lagi", jangan crash.
- **Rate limit** → beri jeda/retry sederhana (opsional untuk MVP).

## 8. Keamanan
- API key **tidak boleh** ditulis langsung di kode; selalu lewat `.env` (dan `.env` masuk `.gitignore`).
- Jangan log isi percakapan sensitif ke file tanpa sepengetahuan user.

## 9. Kemungkinan Pengembangan Lanjutan
- Ganti antarmuka CLI menjadi web app (Streamlit/Flask) tanpa mengubah `chatbot.py`/`memory.py` (karena sudah dipisah dari UI).
- Tambah tool calling (function calling) untuk kemampuan seperti kalkulator atau pencarian data.
- Tambah dukungan multi-provider (OpenAI, model lokal via Ollama) dengan membuat interface abstrak di `chatbot.py`.
