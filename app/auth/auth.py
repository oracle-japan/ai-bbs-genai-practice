import requests
import base64
from os import getenv
from dotenv import load_dotenv

load_dotenv()
IDENTITY_DOMAINS_HOST = getenv('IDENTITY_DOMAINS_HOST')
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')

def get_access_token(api_endpoint: str):
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
    payload = f'grant_type=client_credentials&scope={api_endpoint}/genaiagent'
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
