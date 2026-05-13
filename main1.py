import streamlit as st
from orchestration.supervisor import graph
from mcp_client.tool_executor import initialize_mcp

st.title("AI Multi-Agent Assistant")

query = st.chat_input("Ask something")


if "mcp_initialized" not in st.session_state:
    initialize_mcp()
    st.session_state.mcp_initialized = True
    
if query:
    state = {
        "messages": [{"role": "user", "content": query}],
        "route": None
    }

    result = graph.invoke(state)

    st.write(result["messages"][-1].content)