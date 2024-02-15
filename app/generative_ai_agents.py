import streamlit as st
import requests
from os import getenv
from dotenv import load_dotenv
import auth

load_dotenv()
AGENT_ID = getenv('GEN_AI_AGENTS_ID')
API_ENDPOINT = getenv('GEN_AI_AGENTS_ENDPOINT')
COMPARTMENT_ID = getenv('COMPARTMENT_ID')
GENERATION_MODEL_OCID = getenv('GENERATION_MODEL_OCID')

def generate_text(query: str, access_token: str):
    """Invoke chat endpoint"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json'
    }
    payload = {
        'agentId': AGENT_ID,
        'query': query,
        'shouldReturnSearchDocuments': True,
        'generateTextParameter': {
            'maxTokens': 500
        }
    }
    response = requests.post(
        url=f'{API_ENDPOINT}/20240331/actions/chat',
        json=payload,
        headers=headers,
        verify=False,
    )
    if not response.status_code == 200:
        raise Exception('Failed to obtain query response.')
    else:
        return response.json()

def chat():
    st.title("💬 Generative AI Service w/ AI Agents")
    access_token = auth.get_access_token(API_ENDPOINT)
    if prompt := st.chat_input("What's up?"):
        st.session_state.chat_with_messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            response = generate_text(prompt, access_token)
            message_placeholder.markdown(response['output'])
