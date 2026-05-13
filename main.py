import streamlit as st
from uirouter import set_page,get_page
from mcp_client.tool_executor import initialize_mcp
from views import chatview

def init_view():

    if "mcp_initialized" not in st.session_state:
        initialize_mcp()
        st.session_state.mcp_initialized = True

    st.set_page_config(
        page_title= "AI Multi-Agent Assistant",
        page_icon="🤖",
        layout="centered"

    )
    st.markdown(
    """
    <style>
    .tool-call-badge {
        background: #f0f4ff;
        border-left: 3px solid #5b7fff;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #3a4a8a;
        margin-bottom: 6px;
    }
    .stChatMessage { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
    )

    if st.sidebar.button("💬 Chat Assistant"):
        set_page("Chat Assistant")
    if st.sidebar.button("📊 Evaluation"):
        set_page("evaluation")


    page = get_page()
    if page == "Chat Assistant":
        chatview.render()
    elif page == "evaluation":
        st.write("evaulation view")

init_view()        