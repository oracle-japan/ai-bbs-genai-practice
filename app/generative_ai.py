import streamlit as st
from os import getenv
from dotenv import load_dotenv
from oci.auth.signers import InstancePrincipalsSecurityTokenSigner
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference.models import (
    OnDemandServingMode,
    GenerateTextDetails,
    CohereLlmInferenceRequest,
)

load_dotenv()
GEN_AI_INFERENCE_ENDPOINT = getenv('GEN_AI_INFERENCE_ENDPOINT')
COMPARTMENT_ID = getenv('COMPARTMENT_ID')
GENERATION_MODEL_OCID = getenv('GENERATION_MODEL_OCID')

client = GenerativeAiInferenceClient(
    config={},
    signer=InstancePrincipalsSecurityTokenSigner(),
    service_endpoint=GEN_AI_INFERENCE_ENDPOINT
)

def generate_text(query: str):
    response = client.generate_text(
        generate_text_details=GenerateTextDetails(
            compartment_id=COMPARTMENT_ID,
            serving_mode=OnDemandServingMode(
                model_id=GENERATION_MODEL_OCID
            ),
            inference_request=CohereLlmInferenceRequest(
                prompt=query,
                is_stream=False,
                num_generations=1,
                max_tokens=500
            )
        )
    )
    if not response.status == 200:
        raise Exception("Failed to obtain query response.")
    return response.data.inference_response.generated_texts[0]

def chat():
    st.title("💬 Generative AI Service")
    if prompt := st.chat_input("What's up?"):
        st.session_state.chat_messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            response = generate_text(prompt)
            message_placeholder.markdown(response.text)
