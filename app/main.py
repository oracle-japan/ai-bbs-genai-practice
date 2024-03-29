import streamlit as st
import streamlit_antd_components as sac
from os import getenv
from dotenv import load_dotenv

import generative_ai
import generative_ai_agents
import ai_vector_search_langchain as ai_vector_search_langchain
import ai_vector_search_llamaindex as ai_vector_search_llamaindex
import rinna

load_dotenv()
AGENT_ID = getenv("GEN_AI_AGENTS_ID")
API_ENDPOINT = getenv("GEN_AI_AGENTS_ENDPOINT")

with st.sidebar.container():
    menu = sac.menu([
        sac.MenuItem(label="OCI Generative AI Service"),
        sac.MenuItem(label="OCI Generative AI Service + AI Agents"),
        sac.MenuItem(label="Oracle Database 23c AI Vector Search w/ LangChain"),
        sac.MenuItem(label="Oracle Database 23c AI Vector Search w/ LlamaIndex"),
        sac.MenuItem(label="rinna/japanese-gpt2-small")
    ],
    index=0
)

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_with_messages" not in st.session_state:
    st.session_state.chat_with_messages = []

if __name__ == "__main__":
    if menu == "OCI Generative AI Service":
        generative_ai.chat()
    if menu == "OCI Generative AI Service + AI Agents":
        generative_ai_agents.chat()
    if menu == "Oracle Database 23c AI Vector Search w/ LangChain":
        ai_vector_search_langchain.chat()
    if menu == "Oracle Database 23c AI Vector Search w/ LlamaIndex":
        ai_vector_search_llamaindex.chat()
    if menu == "rinna/japanese-gpt2-small":
        rinna.chat()
