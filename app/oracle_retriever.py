from os import getenv
from dotenv import load_dotenv
from langchain_core.retrievers import BaseRetriever
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings.oci_generative_ai import OCIGenAIEmbeddings
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_community.llms import OCIGenAI
from typing import List
import oracledb

load_dotenv()
COMPARTMENT_ID = getenv("COMPARTMENT_ID")
SERVICE_ENDPOINT = getenv("GEN_AI_INFERENCE_ENDPOINT")
UN = getenv('DB_USERNAME')
PW = getenv('DB_PASSWORD')
DSN = getenv('DB_DSN')
TNS_ADMIN = getenv('TNS_ADMIN')

class OracleRetriever(BaseRetriever):
    # for cache
    documents = [Document]
    
    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        # clear cache.
        self.documents = []
        embeddings = OCIGenAIEmbeddings(
            model_id="cohere.embed-english-v3.0",
            service_endpoint=SERVICE_ENDPOINT,
            compartment_id=COMPARTMENT_ID,
            auth_type="INSTANCE_PRINCIPAL"
        )
        query_v = embeddings.embed_query(text=query)
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
                        self.documents.append(Document(page_content=row["TEXT"], metadata={
                            "id": row["ID"],
                            "title": row["TITLE"],
                            "category": row["CATEGORY"],
                            "url": row["URL"]
                        }))
                    return self.documents

