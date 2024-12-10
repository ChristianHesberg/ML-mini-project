from dotenv import load_dotenv
import os

load_dotenv()

LLM_CONFIG_AZURE = {
    "model": "gpt-4o",
    "api_type": "azure",
    "api_key": os.getenv("GPT_API_KEY"),
    "base_url": os.getenv("GPT_ENDPOINT"),
    "api_version": "2024-08-01-preview",
    "tags": ["gpt4o", "openai"]
}

LLM_CONFIG_LOCAL = {
    "model": "mistral-small:latest",
    "client_host": "127.0.0.1:11434",
    "api_type": "ollama",
    "seed": 42,
    "stream": False,
    "native_tool_calls": False,
    "tags": ["mistral", "local"]
}

config_list = [
    LLM_CONFIG_AZURE,
    LLM_CONFIG_LOCAL
]

