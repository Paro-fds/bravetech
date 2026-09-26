FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code backend et des maquettes officielles de cursus
COPY backend/ ./backend/
COPY cursus/ ./cursus/

EXPOSE 8000

# Commande de démarrage avec serveur ASGI uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
