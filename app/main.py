from fastapi import FastAPI

# Créer l'application FastAPI
app = FastAPI(
    title="Biomed RAG Support API",
    description="API pour le support biomédical avec RAG",
    version="1.0.0"
)

@app.get("/")
def root():
    """Point d'entrée principal"""
    return {
        "status": "ok",
        "message": "Biomed RAG API is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}