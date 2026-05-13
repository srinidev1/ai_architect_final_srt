from orchestration.supervisor import graph
from mcp_client.tool_executor import initialize_mcp

def run_query(query: str):
    state = {
        "messages": [{"role": "user", "content": query}],
        "route": None
    }

    result = graph.invoke(state)
    return result["messages"][-1].content