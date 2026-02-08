from pathlib import Path
from typing import List, Dict
import json
import re
import os

from llama_parse import LlamaParse
print("test1")  # <- AJOUTEZ CECI


def process_document(
    pdf_path: str = "data/documents/document.pdf",
    output_dir: str = "data/processed",
    api_key: str = os.getenv("LLAMA_PARSE_API_KEY"),
) -> List[Dict]:

    print("test2")

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF introuvable: {pdf_file}")

    parser = LlamaParse(
        api_key=api_key,
        result_type="markdown",
        parsing_instruction="Extract clean text and tables. Ignore decorative images.",
    )

    documents = parser.load_data(str(pdf_file))
    print("test3")

    docs = []

    for doc in documents:
        text = doc.text

        if not text or not text.strip():
            continue

        text = re.sub(r"\n?\s*\d+\s*\n?", "\n", text)
        text = re.sub(r"\s+", " ", text)

        docs.append(
            {
                "type": "parsed_document",
                "content": text.strip(),
            }
        )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / f"{pdf_file.stem}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    return docs


def main():
    print("eeeyoooo")
    result = process_document("data/documents/document.pdf")
    print("eeeyooo 2")
    print("Nombre de chunks extraits :", len(result))
    if len(result) > 0:
        print("\nPremier élément :\n", result[0])
    else:
        print("Aucun chunk extrait ! Vérifie le PDF et la clé API.")

if __name__ == "__main__":
    main()
