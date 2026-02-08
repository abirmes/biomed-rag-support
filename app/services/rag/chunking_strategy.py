from sklearn.metrics.pairwise import cosine_similarity

def split_paragraphs(text: str) -> list[str]:
    return [
        p.strip()
        for p in text.split("\n\n")
        if len(p.strip()) > 60
    ]

def semantic_chunk(paragraphs, embeddings, threshold=0.72):
    print(f"   🔍 Génération des embeddings pour {len(paragraphs)} paragraphes...")
    vectors = embeddings.embed_documents(paragraphs)
    print(f"   ✅ Embeddings générés")

    chunks = []
    current_chunk = [paragraphs[0]]

    for i in range(1, len(paragraphs)):
        similarity = cosine_similarity(
            [vectors[i - 1]],
            [vectors[i]]
        )[0][0]
        
        print(f"   📊 Similarité para {i-1} -> {i}: {similarity:.3f} (threshold: {threshold})")

        if similarity >= threshold:
            current_chunk.append(paragraphs[i])
            print(f"      ➡️  Ajouté au chunk actuel (total: {len(current_chunk)} paras)")
        else:
            chunks.append(" ".join(current_chunk))
            print(f"      🆕 Nouveau chunk créé (chunk #{len(chunks)})")
            current_chunk = [paragraphs[i]]

    chunks.append(" ".join(current_chunk))
    print(f"   ✅ Dernier chunk ajouté")
    return chunks

