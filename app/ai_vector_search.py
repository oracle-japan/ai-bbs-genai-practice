import streamlit as st
from os import getenv
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.oci_generative_ai import OCIGenAI
from langchain_community.embeddings.oci_generative_ai import OCIGenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
import oracledb

load_dotenv()
COMPARTMENT_ID = getenv("COMPARTMENT_ID")
SERVICE_ENDPOINT = getenv("GEN_AI_INFERENCE_ENDPOINT")
UN = getenv('DB_USERNAME')
PW = getenv('DB_PASSWORD')
DSN = getenv('DB_DSN')
TNS_ADMIN = getenv('TNS_ADMIN')

def generate_text(query: str):
    query_v = embedding(query)
    context = ai_vector_search(query_v=query_v)
    template = """Answer the question based only on the following context:
    {context}

    Question: {query}
    """
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "query"]
    )
    llm = OCIGenAI(
        auth_type="INSTANCE_PRINCIPAL",
        service_endpoint=SERVICE_ENDPOINT,
        model_id="cohere.command",
        compartment_id=COMPARTMENT_ID,
        model_kwargs={
            'max_tokens': 500
        }
    )
    chain = prompt | llm | StrOutputParser()
    output = chain.invoke({"context": context['text'], "query": query})
    return {'output': output, 'url': context['url']}

def embedding(text: str):
    embeddings = OCIGenAIEmbeddings(
        model_id="cohere.embed-english-v3.0",
        service_endpoint=SERVICE_ENDPOINT,
        compartment_id=COMPARTMENT_ID,
        auth_type="INSTANCE_PRINCIPAL"
    )
    return embeddings.embed_query(text=text)

def ai_vector_search(query_v: str):
    context = list()
    with oracledb.connect(user=UN, password=PW, dsn=DSN, config_dir=TNS_ADMIN) as connection:
        with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        ID,
                        TITLE,
                        CATEGORY,
                        URL,
                        TEXT
                    FROM
                        OCI_SERVICES
                    ORDER BY VECTOR_DISTANCE(TEXT_V, :query)
                    FETCH FIRST 1 ROWS ONLY
                """, query=f"{query_v}")
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                for row in cursor:
                    context.append({'text': row['TEXT'], 'url': row['URL']})
                return context[0]
                

def chat():
    st.title("💬 Oracle Database 23c - AI Vector Search")
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
