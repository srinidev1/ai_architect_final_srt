import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

DIAL_API_KEY = os.getenv('DIAL_API_KEY')
DIAL_MODEL =  os.getenv('AZURE_MODEL', "gpt-4")
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT','https://ai-proxy.lab.epam.com')
API_VERSION = os.getenv('AZURE_API_VERSION', '2024-08-01-preview')

orchestrator_llm = init_chat_model(
    "ollama:llama3.2"
)

response_generator_llm = AzureOpenAI(
    api_key         = DIAL_API_KEY,
    api_version     = API_VERSION,
    azure_endpoint  = AZURE_ENDPOINT
)