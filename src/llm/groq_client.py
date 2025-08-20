from langchain_groq import ChatGroq
from src.config.settings import settings
from src.common.custom_exception import CustomException


def get_groq_llm():
    if not settings.GROQ_API_KEY:
        raise CustomException("GROQ_API_KEY not found in environment variables")
    
    if not settings.GROQ_API_KEY.startswith('gsk_'):
        raise CustomException("Invalid GROQ API key format. Key should start with 'gsk_'")
    
    return ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model = settings.MODEL_NAME,
        temperature = settings.TEMPERATURE,
    )
    

