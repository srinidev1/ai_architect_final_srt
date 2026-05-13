import asyncio
from services.weather_service import fetch_weather_response

def weather_agent(state):
    last_message = state["messages"][-1]

    #print(f"Weather agent received message: {last_message.content}")

    result = fetch_weather_response(last_message.content,[])
    
    return {
        "messages": [
            {"role": "assistant", "content": str(result)}
        ]
    }