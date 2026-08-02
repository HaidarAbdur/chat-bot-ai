# Chatbot AI (Python)

Chatbot sederhana berbasis Python yang menggunakan Anthropic Claude API sebagai otak percakapannya. Berjalan di terminal (CLI), mengingat konteks percakapan selama sesi berlangsung.

## Fitur
- Chat interaktif lewat terminal
- Riwayat percakapan tetap nyambung dalam satu sesi
- System prompt/persona bisa dikustomisasi
- Konfigurasi aman lewat file `.env`

## Struktur Projek
```
chatbot-ai/
├── README.md
├── PRD.md          # dokumen kebutuhan produk
├── DESIGN.md        # dokumen desain teknis
├── requirements.txt
├── .env.example
├── src/
│   ├── main.py
│   ├── chatbot.py
│   ├── config.py
│   └── memory.py
└── tests/
    └── test_chatbot.py
```

## Persiapan

1. **Clone / masuk ke folder projek**
   ```bash
   cd chatbot-ai
   ```

2. **Buat virtual environment (disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Buat file `.env`**
   ```bash
   cp .env.example .env
   ```
   Lalu isi `ANTHROPIC_API_KEY` dengan API key kamu (dapatkan di [console.anthropic.com](https://console.anthropic.com)).

## Menjalankan Chatbot

```bash
python -m src.main
```

Ketik pesan lalu tekan Enter. Perintah khusus:
- `/reset` — hapus riwayat percakapan
- `/exit` — keluar dari program

## Menjalankan Test

```bash
pytest
```

## Roadmap
Lihat `PRD.md` bagian Roadmap untuk rencana pengembangan lanjutan (persistent memory, streaming, tool calling, UI web).

## Lisensi
Bebas dipakai untuk belajar/personal project.
