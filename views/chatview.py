import streamlit as st
from pathlib import Path
from orchestration.graph_runner import run_query

def _init_session():
    """Bootstrap session state keys used by this view."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []       
    if "source_docs" not in st.session_state:
        st.session_state["source_docs"] = []    
    if "pending_input" not in st.session_state:  
        st.session_state["pending_input"] = None

def _init_page_config():
    st.set_page_config(
        page_title="AI Multi-Agent Assistant",
        page_icon="🤖",
        layout="centered",
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

    st.title("AI Assistant")
    st.divider()
    st.caption("Chat with your AI assistant powered by Annual Report Knowledge Base.")
    with st.expander("💡 Example questions", expanded=False):
        examples = [
            ("What's Non-stock corporations franchise tax?", "What's Non-stock corporations franchise tax?"),
            ("Due date for foreign annual reports?", "Due date for foreign annual reports?"),
            ("What is the weather in Buffalo", "What is the weather in Buffalo"),
            ("For India, what is the breakdown of disaster types by frequency and total deaths over time?", "For India, what is the breakdown of disaster types by frequency and total deaths over time?"),
            ("Which 5 natural disasters caused the highest total deaths, and what countries and disaster types do they belong to?", "Which 5 natural disasters caused the highest total deaths, and what countries and disaster types do they belong to?"),
            ("Which country has the highest number of natural disasters recorded between 1900 and 2021?", "Which country has the highest number of natural disasters recorded between 1900 and 2021?"),
            ("What is the minimum franchise tax? ", "What is the minimum franchise tax?"),
            ("What is the Annual report Filing Fee in New York?", "lets do the role play, now you are New York filing assistant , what is the annual report filing fee in new york")
        ]
        for display_text, query_value in examples:
            if st.button(display_text, key=f"ex_{display_text}"):
                st.session_state.pending_input = query_value
                st.rerun()

    st.divider()


def render():
    _init_session()

    _init_page_config()


    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = None

    if st.session_state.pending_input:
        user_input = st.session_state.pending_input
        st.session_state.pending_input = None

    typed_input = st.chat_input("Ask me anything about Annual Reports…")

    if typed_input and typed_input.strip():
        user_input = typed_input.strip()

    if user_input:
        _handle_question(user_input)


def _handle_question(question: str) -> None:
    """
    Append the user message, call answer_question, append the assistant reply,
    all in session state.
    """
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    history = st.session_state["messages"][:-1]

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
              answer = run_query(query=question)
        st.markdown(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
   