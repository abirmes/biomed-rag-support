from .document_processor import extract_text_from_pdf
from .chunking_strategy import split_paragraphs, semantic_chunk
from .embeddings import embeddings
from .vector_store import get_vectorstore
from .retriever import retrieve
from .llm_service import llm

def index_pdf(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    paragraphs = split_paragraphs(text)
    chunks = semantic_chunk(paragraphs, embeddings)

    vectordb = get_vectorstore()
    vectordb.add_texts(
        texts=chunks,
        metadatas=[{"source": pdf_path}] * len(chunks)
    )
    vectordb.persist()

def self_rag(query: str):
    docs = retrieve(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Tu es un expert en équipements biomédicaux.
Réponds uniquement à partir du contexte fourni.
Si l'information n'existe pas, dis-le clairement.

Contexte:
{context}

Question:
{query}
"""

    answer = llm(prompt)

    critique_prompt = f"""
Évalue la réponse suivante.
Réponds uniquement par un nombre entre 0 et 1.

Réponse:
{answer}
"""
    score = float(llm(critique_prompt).strip())

    if score < 0.7:
        refined_query = query + " procédure technique"
        docs = retrieve(refined_query, k=10)
        context = "\n\n".join(d.page_content for d in docs)
        answer = llm(prompt)

    return answer
