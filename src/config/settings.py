import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = "llama-3.1-8b-instant"
    TEMPERATURE: float = 0.9
    MAX_RETIRES: int = 3
    # TOP_P: float = 0.95
    # TOP_K: int = 40
   
   
settings = Settings()