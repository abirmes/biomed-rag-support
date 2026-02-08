# biomed-rag-support


BIOMED-RAG-SUPPORT/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Point d'entrée FastAPI
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py              # Configuration centralisée
│   │   └── database.py              # Configuration DB
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py              # JWT, hashing
│   │   ├── exceptions.py            # Exceptions personnalisées
│   │   └── dependencies.py          # Dépendances FastAPI
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # Modèle User
│   │   └── query.py                 # Modèle Query
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                  # Schémas Pydantic User
│   │   ├── query.py                 # Schémas Pydantic Query
│   │   └── rag.py                   # Schémas RAG
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py # Endpoints auth
│   │   ├── queries.py           # Endpoints queries        
│   │   └── admin.py             # Endpoints admin
│   │   
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py          # Logique authentification
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── document_processor.py    # Prétraitement PDF
│   │   │   ├── chunking_strategy.py     # Stratégies de chunking
│   │   │   ├── embeddings.py            # Génération embeddings
│   │   │   ├── vector_store.py          # Gestion ChromaDB
│   │   │   ├── retriever.py             # Récupération chunks
│   │   │   ├── reranker.py              # Reranking
│   │   │   ├── llm_service.py           # Interaction LLM
│   │   │   └── rag_pipeline.py          # Pipeline complet
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── query_repository.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_rag_pipeline.py
│   └── test_chunking.py
│
├── data/
│   ├── documents/                   # PDF sources
│   └── processed/                   # Documents traités
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .env
├── requirements.txt
├── README.md
└── alembic/                         # Migrations DB
    └── versions/