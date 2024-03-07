import streamlit as st
from os import getenv
from dotenv import load_dotenv
import requests

load_dotenv()
RINNA_ENDPOINT = getenv('RINNA_ENDPOINT')

def generate_text(query: str):
    response = requests.post(RINNA_ENDPOINT + "/api/generate", json={"query": query})
    if not response.status_code == 200:
        raise Exception("Failed to obtain query response.")
    return response.json()

def chat():
    st.title("💬 rinna/japanese-gpt2-small")
    if prompt := st.chat_input("What's up?"):
        st.session_state.chat_messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            response = generate_text(prompt)
            message_placeholder.markdown(response["generated_text"])
