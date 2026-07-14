# ============================================================================
# 🐳 DOCKERFILE - LOCAL & PRODUCTION BUILD
# Sama untuk local dan production, perbedaan terletak di environment variables
# ============================================================================

# Multi-stage build untuk optimasi ukuran image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install sistem dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (7860 untuk HF Spaces, dan local development)
EXPOSE 7860

# Environment variables - Default untuk local development
# Untuk production (HF Spaces), override via environment variables
ENV PYTHONUNBUFFERED=1

# 🏠 LOCAL: OLLAMA_URL=http://ollama:11434 (dari docker-compose)
# ☁️  PRODUCTION: OLLAMA_URL=<external-url> (set di HF Spaces)
ENV OLLAMA_URL=http://ollama:11434

# 🏠 LOCAL: DATABASE_URL=mysql+pymysql://root:root@mysql:3306/chatbot_db (dari docker-compose)
# ☁️  PRODUCTION: DATABASE_URL=<cloud-url> (set di HF Spaces)
# Lihat app/database.py untuk logic

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/docs || exit 1

# Run aplikasi dengan port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
