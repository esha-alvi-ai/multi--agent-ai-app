# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# === Application Configuration ===
APP_NAME = "Multi-Agent AI App"
VERSION = "1.0.0"
DEBUG_MODE = True

# === AI Model Config ===
# You can swap this to other LLMs if needed
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")  
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# === Multi-Agent Settings ===
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", 60))  # seconds
MAX_AGENT_INTERACTIONS = int(os.getenv("MAX_AGENT_INTERACTIONS", 5))

# === Logging Settings ===
LOG_FILE = "logs/app.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# === Database / Storage Config (Optional) ===
DB_URI = os.getenv("DB_URI", "sqlite:///app.db")

# === Utility Function ===
def validate_config():
    """Ensure critical configurations are set."""
    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY. Please set it in environment variables or .env file.")

