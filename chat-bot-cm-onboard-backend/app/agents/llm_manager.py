# llm setup

from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.enums.ai_models import AIModels


def get_llm(temperature:float=0, model: AIModels = AIModels.GPT_5_NANO):

    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in the configuration.")

    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=model,
        temperature=temperature
    )