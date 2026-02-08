from .vector_store import get_vectorstore

def retrieve(query: str, k: int = 8):
    vectordb = get_vectorstore()
    return vectordb.similarity_search(query, k=k)
