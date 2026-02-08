import json

from chunking_strategy import split_paragraphs, semantic_chunk
from embeddings import embeddings
from vector_store import get_vectorstore


def index_from_json(json_path: str = "data/processed/document.json"):

    with open(json_path, "r", encoding="utf-8") as f:
        docs = json.load(f)


    full_text = "\n\n".join(doc["content"] for doc in docs)
    print(f"  Texte total: {len(full_text)} caractères\n")

    paragraphs = split_paragraphs(full_text)

    if paragraphs:
        print(f"   Exemple: {paragraphs[0][:80]}...\n")

    chunk_size = 1000      
    chunk_overlap = 200    

    chunks = []

    for para in paragraphs:
        if len(para) <= chunk_size:
            chunks.append(para)
        else:
            start = 0
            while start < len(para):
                end = start + chunk_size
                chunks.append(para[start:end])
                start += (chunk_size - chunk_overlap) 

    if chunks:
        print(f"   Premier chunk: {chunks[0][:100]}...")
    print()


    vectordb = get_vectorstore()

    metadatas = [
        {"source": json_path, "chunk_id": i}
        for i in range(len(chunks))
    ]

    vectordb.add_texts(texts=chunks, metadatas=metadatas)
    vectordb.persist()


    return {
        "total_chars": len(full_text),
        "num_paragraphs": len(paragraphs),
        "num_chunks": len(chunks),
        "json_path": json_path,
    }


if __name__ == "__main__":
    result = index_from_json("/app/data/processed/document.json")

    print(f"   - Caractères: {result['total_chars']}")
    print(f"   - Paragraphes: {result['num_paragraphs']}")
    print(f"   - Chunks: {result['num_chunks']}")
