import streamlit as st
from os import getenv
from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.core import PromptTemplate, VectorStoreIndex, Settings
from retriever.oracle_query_engine import OracleQueryEngine

load_dotenv()
COHERE_API_KEY = getenv("COHERE_API_KEY")

def generate_text(query: str):
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt_template = PromptTemplate(template=template)
    llm = Cohere(api_key=COHERE_API_KEY)
    Settings.llm = llm
    query_engine = OracleQueryEngine()
    context = query_engine.query(query)
    prompt = prompt_template.format(context=context.response, question=query)
    response = llm.complete(prompt, formatted=True)
    return {"output": response.text, "url": context.metadata["url"]}
    

def chat():
    st.title("💬 Oracle Database 23c - AI Vector Search w/ LlamaIndex")
    if prompt := st.chat_input('What"s up?'):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = generate_text(prompt)
            output_template = f"""
                {response["output"]}  
                ----------  
                ref:  
                {response["url"]}
            """
            message_placeholder.markdown(output_template)
