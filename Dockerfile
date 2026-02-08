FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie du code source
COPY . .

# Création des dossiers nécessaires
RUN mkdir -p /app/data /app/uploads /app/chroma_db

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]