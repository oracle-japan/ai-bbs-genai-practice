import streamlit as st
import requests
import base64
from os import getenv
from dotenv import load_dotenv

load_dotenv()
IDENTITY_DOMAINS_HOST = getenv('IDENTITY_DOMAINS_HOST')
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
AGENT_ID = getenv('GEN_AI_AGENTS_ID')
API_ENDPOINT = getenv('GEN_AI_AGENTS_ENDPOINT')

st.title('AI Brown Bag Seminar #7')

def get_access_token():
    """Obtain an access token using client credentials grant"""
    well_known_response = requests.get(
        url=IDENTITY_DOMAINS_HOST + '/.well-known/openid-configuration'
    )
    if not well_known_response.status_code == 200:
        raise Exception('Failed to obtain openid connect configuration')
    token_endpoint = well_known_response.json().get('token_endpoint')
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    payload = f'grant_type=client_credentials&scope={API_ENDPOINT}/genaiagent'
    token_endpoint_response = requests.post(
        url=token_endpoint,
        headers=headers,
        data=payload,
        verify=True
    )
    if not token_endpoint_response.status_code == 200:
        raise Exception('Failed to obtain access token')
    else:
        access_token = token_endpoint_response.json().get('access_token')
        return access_token

def generative_ai_agent(query: str, access_token: str):
    """Invoke chat endpoint"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json'
    }
    payload = {
        'agentId': AGENT_ID,
        'query': query,
        'shouldReturnSearchDocuments': True,
    }
    response = requests.post(
        url=f'{API_ENDPOINT}/20240331/actions/chat',
        json=payload,
        headers=headers,
        verify=False,
        stream=True
    )
    if not response.status_code == 200:
        raise Exception('Failed to obtain query response.')
    else:
        return response.json()

def chat():
    access_token = get_access_token()
    if prompt := st.chat_input("What's up?"):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            response = generative_ai_agent(prompt, access_token)
            message_placeholder.markdown(response['output'])
        st.session_state.messages.append({'role': 'assistant', 'content': response['output']})

if __name__ == '__main__':
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from history an app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    chat()
