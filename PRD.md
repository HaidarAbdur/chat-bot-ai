# PRD — Chatbot AI (Python)

## 1. Latar Belakang
Projek personal untuk membangun chatbot berbasis AI menggunakan Python, dengan tujuan belajar arsitektur aplikasi AI sederhana sekaligus punya deliverable yang bisa dipakai/dipamerkan.

## 2. Tujuan (Goals)
- Membuat chatbot CLI (command line) yang bisa diajak ngobrol secara natural.
- Chatbot bisa mengingat konteks percakapan dalam satu sesi (short-term memory).
- Struktur kode rapi & mudah dikembangkan (misalnya nanti ditambah UI web).

## 3. Non-Goals (di luar cakupan versi awal)
- Tidak membangun UI web/mobile dulu (fokus CLI dulu, UI bisa jadi fase 2).
- Tidak melatih model sendiri dari nol (pakai model AI yang sudah ada via API).
- Tidak menangani banyak user sekaligus (single-user, local use).

## 4. Target Pengguna
- Diri sendiri (developer/pembelajar) sebagai user utama.
- Bisa dipakai sebagai portofolio/demo ke orang lain.

## 5. Fitur Utama (MVP)
| # | Fitur | Prioritas |
|---|-------|-----------|
| 1 | Chat via terminal (input/output teks) | Wajib |
| 2 | Riwayat percakapan disimpan selama sesi berjalan | Wajib |
| 3 | System prompt/persona yang bisa dikustomisasi | Wajib |
| 4 | Konfigurasi API key lewat file `.env` | Wajib |
| 5 | Penanganan error (koneksi gagal, API key salah, dll) | Wajib |
| 6 | Simpan riwayat chat ke file (opsional, persistent memory) | Opsional |
| 7 | Streaming response (jawaban muncul sedikit-sedikit) | Opsional |
| 8 | Tool/function calling (misal chatbot bisa hitung matematika) | Opsional (fase 2) |
| 9 | UI web sederhana (Flask/Streamlit) | Opsional (fase 2) |

## 6. User Stories
- Sebagai user, saya ingin mengetik pertanyaan dan mendapat jawaban dari AI, supaya saya bisa berdiskusi seperti chat biasa.
- Sebagai user, saya ingin chatbot ingat apa yang saya bicarakan sebelumnya dalam sesi yang sama, supaya percakapan terasa nyambung.
- Sebagai user, saya ingin bisa mengganti "kepribadian" chatbot lewat system prompt, supaya chatbot bisa disesuaikan untuk kebutuhan berbeda (asisten belajar, teman ngobrol, dll).
- Sebagai developer, saya ingin API key tidak ter-hardcode di kode, supaya aman saat kode di-share/upload ke GitHub.

## 7. Metrik Keberhasilan (sederhana, karena projek kecil)
- Chatbot berjalan tanpa error untuk skenario normal.
- Respons AI relevan dengan pertanyaan (evaluasi manual/subjektif).
- Struktur kode terpisah rapi (main, chatbot logic, config) — mudah dibaca ulang 1 bulan kemudian.

## 8. Batasan & Risiko
- Butuh koneksi internet & API key (karena pakai model AI via API, bukan lokal).
- Biaya API (meski kecil untuk pemakaian personal) — perlu diawasi penggunaan token.
- Riwayat chat di memori akan hilang saat program ditutup, kecuali fitur simpan-ke-file diaktifkan.

## 9. Roadmap Singkat
1. **Fase 1 (MVP)**: Chatbot CLI dasar dengan memory per-sesi.
2. **Fase 2**: Persistent memory (simpan ke file/DB), streaming response.
3. **Fase 3**: Tool calling (kalkulator, pencarian web, dsb).
4. **Fase 4**: UI web sederhana (Streamlit/Flask) di atas logic yang sudah ada.
