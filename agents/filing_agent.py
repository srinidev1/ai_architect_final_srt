from services.filing_service import search_filings


def filing_agent(state):
    last_message = state["messages"][-1]
    result = search_filings(last_message.content,[])

    return {
        "messages": [
            {"role": "assistant", "content": result}
        ]
    }