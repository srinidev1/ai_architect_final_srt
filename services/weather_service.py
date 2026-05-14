import os
from dotenv import load_dotenv
from mcp_client.tool_executor import get_tools_format,handle_tool_call
from utils.models import response_generator_llm,get_response_generator_llm_model
import json

load_dotenv(override=True)

system_message = """
    You are a helpful weather assistant. you have access to a tools that can provide weather information.
    Give short, courteous answers, no more than 1 sentence.
    Always be accurate. If you don't know the answer, say so.
"""

def fetch_weather_response(question: str,history: list[dict]) -> str:
    """
    Fetch a weather response for the given question.
    """
   
    messages = [{"role": "system", "content": system_message}]
    for m in history:
        if m["role"] in ("user", "assistant"):
            messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": question})

    response = response_generator_llm.chat.completions.create(
            messages=messages,            
            model=get_response_generator_llm_model(),
            tools= get_tools_format()
    )    

    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = response_generator_llm.chat.completions.create(
            messages=messages,            
            model=get_response_generator_llm_model()
    )    

    return response.choices[0].message.content



