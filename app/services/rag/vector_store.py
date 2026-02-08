from langchain_community.vectorstores import Chroma
from embeddings import embeddings

def get_vectorstore():
    return Chroma(
        collection_name="biomed_manuals",
        persist_directory="/app/chroma",
        embedding_function=embeddings
    )
