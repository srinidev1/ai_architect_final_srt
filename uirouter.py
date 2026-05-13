import streamlit as st

def get_page():
    params = st.query_params
    return params.get("page", "Chat Assistant")


def set_page(page_name):
    st.query_params["page"] = page_name