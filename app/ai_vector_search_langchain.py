import streamlit as st
from os import getenv
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.oci_generative_ai import OCIGenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from oracle_retriever import OracleRetriever

load_dotenv()
COMPARTMENT_ID = getenv("COMPARTMENT_ID")
SERVICE_ENDPOINT = getenv("GEN_AI_INFERENCE_ENDPOINT")

def generate_text(query: str):
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template=template)
    llm = OCIGenAI(
        auth_type="INSTANCE_PRINCIPAL",
        service_endpoint=SERVICE_ENDPOINT,
        model_id="cohere.command",
        compartment_id=COMPARTMENT_ID,
        model_kwargs={
            'max_tokens': 500
        }
    )
    retriever = OracleRetriever()
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    output = chain.invoke(query)
    documents = retriever.documents
    return {"output": output, "url": documents[0].metadata.get("url", "")}

def chat():
    st.title("💬 Oracle Database 23c - AI Vector Search w/ LangChain")
    if prompt := st.chat_input("What's up?"):
        st.session_state.chat_messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            response = generate_text(prompt)
            output_template = f"""
                {response['output']}  
                ---  
                ref:  
                {response['url']}
            """
            message_placeholder.markdown(output_template)
