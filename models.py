import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv() # loading environment variables (model api(s)) from .env file

# gemini model for high level tasks
gemini_model = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google_genai",
    max_retries=2,
    timeout=2000,
    temperature=0.3,
    api_key=os.environ.get("GEMINI_API_KEY")
)