from dotenv import load_dotenv
import os

load_dotenv()

LLM_CONFIG = {
    "model": "gpt-4o",
    "api_type": "azure",
    "api_key": os.getenv("GPT_API_KEY"),
    "base_url": os.getenv("GPT_ENDPOINT"),
    "api_version": "2024-05-13"
}