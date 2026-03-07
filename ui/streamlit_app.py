

import streamlit as st
import os
import sys

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.graph import build_graph
from app.rag_pipeline import create_vector_store

st.set_page_config(
    page_title="Hellobooks AI Assistant",
    page_icon="📊"
)

st.title("📊 Hellobooks AI Accounting Assistant")

st.write("Ask accounting related questions.")

if not os.path.exists("vectorstore"):
    with st.spinner("Creating knowledge base..."):
        create_vector_store()

graph = build_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask an accounting question")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    result = graph.invoke({
        "question": user_input
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])