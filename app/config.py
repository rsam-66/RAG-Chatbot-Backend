"""
🔧 Application Configuration
Centralized configuration management untuk local development & production
"""

import os
from typing import Optional

# ============================================================================
# 📦 DATABASE CONFIGURATION
# ============================================================================

def get_database_url() -> str:
    """
    🏠 LOCAL: MySQL di Docker atau lokal
    ☁️ PRODUCTION: Cloud database (Railway, PlanetScale, Vercel, Supabase)
    
    Environment Variable: DATABASE_URL
    Default: mysql+pymysql://root:root@mysql:3306/chatbot_db
    
    Examples:
    - MySQL Docker: mysql+pymysql://root:root@mysql:3306/chatbot_db
    - MySQL Lokal: mysql+pymysql://root:password@127.0.0.1:3306/chatbot_db
    - SQLite: sqlite:///./chatbot.db
    - PostgreSQL: postgresql://user:pass@host:5432/database
    """
    return os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@mysql:3306/chatbot_db"
    )


# ============================================================================
# 🤖 OLLAMA CONFIGURATION
# ============================================================================

def get_ollama_url() -> str:
    """
    🏠 LOCAL: Ollama di Docker atau lokal
    ☁️ PRODUCTION: Ollama di server terpisah atau API eksternal
    
    Environment Variable: OLLAMA_URL
    Default: http://ollama:11434
    
    Examples:
    - Docker: http://ollama:11434
    - Lokal (Windows): http://localhost:11434
    - Remote: http://192.168.1.100:11434
    - External: https://api.ollama.provider.com
    """
    return os.getenv("OLLAMA_URL", "http://ollama:11434")


def get_ollama_api_key() -> Optional[str]:
    """
    🔑 OLLAMA_API_KEY (jika menggunakan API berbayar)
    
    Environment Variable: OLLAMA_API_KEY
    Optional, hanya jika Ollama memerlukan authentication
    """
    return os.getenv("OLLAMA_API_KEY")


# ============================================================================
# 🤖 ALTERNATIVE MODEL PROVIDERS
# ============================================================================

def get_hf_model_name() -> Optional[str]:
    """
    🤗 HuggingFace Model Name (jika gunakan HF instead Ollama)
    
    Environment Variable: HF_MODEL_NAME
    Example: mistral-7b, llama2, neural-chat
    """
    return os.getenv("HF_MODEL_NAME")


def get_hf_api_key() -> Optional[str]:
    """
    🔑 HuggingFace API Key (jika gunakan HF Inference API)
    
    Environment Variable: HF_API_KEY
    Get from: https://huggingface.co/settings/tokens
    """
    return os.getenv("HF_API_KEY")


def get_openai_api_key() -> Optional[str]:
    """
    🔑 OpenAI API Key (jika gunakan OpenAI GPT)
    
    Environment Variable: OPENAI_API_KEY
    Get from: https://platform.openai.com/api-keys
    """
    return os.getenv("OPENAI_API_KEY")


def get_model_provider() -> str:
    """
    📍 Model Provider Selection
    
    Environment Variable: MODEL_PROVIDER
    Default: ollama
    
    Options:
    - ollama: Local Ollama
    - huggingface: HuggingFace Inference API
    - openai: OpenAI GPT
    """
    return os.getenv("MODEL_PROVIDER", "ollama")


# ============================================================================
# 🔧 DEBUG & PYTHON SETTINGS
# ============================================================================

def get_debug_mode() -> bool:
    """
    🐛 Debug Mode
    
    Environment Variable: DEBUG
    Default: false
    """
    return os.getenv("DEBUG", "false").lower() == "true"


def get_python_unbuffered() -> bool:
    """
    📺 Python Unbuffered Output
    
    Environment Variable: PYTHONUNBUFFERED
    Default: 1 (enabled)
    """
    value = os.getenv("PYTHONUNBUFFERED", "1")
    return value != "0"


# ============================================================================
# 🔍 Configuration Summary
# ============================================================================

class Config:
    """
    Configuration class untuk easy access
    
    Usage:
    >>> from app.config import Config
    >>> db_url = Config.DATABASE_URL
    >>> ollama_url = Config.OLLAMA_URL
    """
    
    # 📦 Database
    DATABASE_URL = get_database_url()
    
    # 🤖 Ollama
    OLLAMA_URL = get_ollama_url()
    OLLAMA_API_KEY = get_ollama_api_key()
    
    # 🤗 HuggingFace
    HF_MODEL_NAME = get_hf_model_name()
    HF_API_KEY = get_hf_api_key()
    
    # 🔐 OpenAI
    OPENAI_API_KEY = get_openai_api_key()
    
    # 📍 Provider
    MODEL_PROVIDER = get_model_provider()
    
    # 🔧 Debug
    DEBUG = get_debug_mode()
    PYTHONUNBUFFERED = get_python_unbuffered()
    
    @classmethod
    def print_config(cls):
        """Print current configuration (safe, no secrets)"""
        print("\n" + "="*60)
        print("⚙️  Current Configuration")
        print("="*60)
        print(f"📦 Database: {cls.DATABASE_URL.split('@')[1] if '@' in cls.DATABASE_URL else cls.DATABASE_URL}...")
        print(f"🤖 Ollama URL: {cls.OLLAMA_URL}")
        print(f"📍 Model Provider: {cls.MODEL_PROVIDER}")
        print(f"🐛 Debug Mode: {cls.DEBUG}")
        print("="*60 + "\n")


# ============================================================================
# 📝 ENVIRONMENT VARIABLES REFERENCE
# ============================================================================

"""
LOCAL DEVELOPMENT (.env):
====================================
DATABASE_URL=mysql+pymysql://root:root@mysql:3306/chatbot_db
OLLAMA_URL=http://ollama:11434
DEBUG=true
PYTHONUNBUFFERED=1

PRODUCTION (HF Spaces Settings):
====================================
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db
OLLAMA_URL=https://external-ollama.com:11434
DEBUG=false
PYTHONUNBUFFERED=1

ALTERNATIVE - HuggingFace:
====================================
OLLAMA_URL=huggingface
HF_MODEL_NAME=mistral-7b
HF_API_KEY=hf_xxxxxxxxxxxxx

ALTERNATIVE - OpenAI:
====================================
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
"""

if __name__ == "__main__":
    # Print current configuration
    Config.print_config()
