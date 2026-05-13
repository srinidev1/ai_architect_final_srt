from services.disaster_event_service import search_events

def disaster_event_agent(state):
    last_message = state["messages"][-1]

    result = search_events(last_message.content,[])

    return {
        "messages": [
            {"role": "assistant", "content": str(result)}
        ]
    }

