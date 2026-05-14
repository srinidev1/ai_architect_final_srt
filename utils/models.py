import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import AzureChatOpenAI

load_dotenv()

DIAL_API_KEY = os.getenv('DIAL_API_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT','https://ai-proxy.lab.epam.com')
API_VERSION = os.getenv('AZURE_API_VERSION', '2024-08-01-preview')
ORCHESTRATOR_MODEL = os.getenv('ORCHESTRATOR_MODEL', 'gemini-2.5-flash-lite')


#orchestrator_llm = init_chat_model(
    #"ollama:llama3.2"
#)

orchestrator_llm = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=DIAL_API_KEY,
    api_version=API_VERSION,
    model=ORCHESTRATOR_MODEL,
    temperature=0
)


response_generator_llm = AzureOpenAI(
    api_key         = DIAL_API_KEY,
    api_version     = API_VERSION,
    azure_endpoint  = AZURE_ENDPOINT
)

judge_llm = AzureOpenAI(
    api_key         = DIAL_API_KEY,
    api_version     = API_VERSION,
    azure_endpoint  = AZURE_ENDPOINT
)

def get_response_generator_llm_model() -> str:
    return os.getenv('RESPONSE_LLM_MODEL', "gpt-4")

def get_judge_llm_model() -> str:
    return os.getenv('JUDGE_MODEL', "gemini-2.5-flash")
