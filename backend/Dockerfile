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

# Migrations de la base (US-023), puis serveur ASGI uvicorn : si une migration échoue, l'API ne démarre pas
CMD ["sh", "-c", "python -m backend.scripts.migrer && exec uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
