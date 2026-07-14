---
title: RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# RAG Chatbot

## 📌 Stack

- FastAPI (API Framework)
- LangChain (RAG Orchestrator)
- ChromaDB (Vector Database)
- Sentence Transformers (Embedding)
- Ollama (LLM Local)

---

## ⚙️ Setup

### 1. Install dependencies

pip install -r requirements.txt

### 2. Build vector database

python app/initialize.py

### 3. Run API

uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

---

## 📂 Data Format

Supported:

- .txt
- .docx
- .toon (JSON)

---

## 🔁 RAG Flow

1. Documents loaded
2. Split into chunks
3. Embedded with multilingual model
4. Stored in ChromaDB
5. Query → embedding → similarity search
6. Retrieved context → sent to LLM
7. Answer returned

---

## 🧠 Embedding Model

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2  
Supports Bahasa Indonesia

---

## 🎮 Endpoint

✅ POST /Initialize

Membangun vector database.

<!--  -->

✅ POST /chat

Mengirim pertanyaan ke chatbot.

Request body:

{
"question": "Apa saja paket wisata yang tersedia?"
}

Response contoh:

{
"answer": "...jawaban dari LLM...",
"sources": ["potongan dokumen 1", "potongan dokumen 2"]
}

---

---

## 🐳 Docker Deployment

### Local Testing dengan Docker Compose

```bash
docker-compose up -d
```

Akses: http://localhost:7860/docs

### Deploy ke Hugging Face Spaces (Recommended)

**Step 1: Buat Space baru**

- Buka https://huggingface.co/spaces
- Klik "Create new Space"
- Pilih **"Docker"** sebagai runtime
- Klik "Create Space"

**Step 2: Push code via Git** (HF akan otomatis build Dockerfile)

```bash
# Initialize git
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit: RAG Chatbot"

# Connect ke HF Space
git remote add origin https://huggingface.co/spaces/<username>/<space-name>

# Push ke HF (HF otomatis detect Dockerfile dan build!)
git push -u origin main
```

**Step 3: Set Environment Variable** di HF Spaces Settings:

- `OLLAMA_URL`: URL Ollama server
  - Lokal: `http://localhost:11434`
  - Eksternal: `https://your-ollama-server.com`

**Step 4: Initialize Vector Database** (first time only)

- Jalankan `/initialize` endpoint di HF Space
- Atau SSH ke container dan jalankan: `python app/initialize.py`

### Alternative: Manual Docker Push

Jika ingin push ke Docker registry sendiri:

```bash
docker build -t registry.hf.space/<username>/<space-name> .
docker push registry.hf.space/<username>/<space-name>
```

---

## 🚀 Production Upgrade Ideas

- Add conversation memory
- Add metadata filtering
- Add authentication
- Use async FastAPI
- Add API rate limiting
