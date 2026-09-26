"""Point d'entrée de l'application FastAPI — FDS Portail.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import api_v1_router
from backend.dal.cursus_repository_sql import SQLAlchemyCursusRepository

app = FastAPI(
    title="FDS Portail API — Faculté des Sciences (UEH)",
    description="API REST officielle du portail d'information et d'inscription dématérialisée de la FDS-UEH.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS pour permettre au frontend (Vite, local, web) de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes v1
app.include_router(api_v1_router)


@app.on_event("startup")
def on_startup():
    """Initialise le repository et la base de données au démarrage."""
    SQLAlchemyCursusRepository()


@app.get("/", tags=["Santé & Info"])
def root():
    return {
        "service": "FDS Portail API",
        "statut": "actif",
        "documentation": "/docs",
        "api_v1": "/api/v1/cursus"
    }


@app.get("/health", tags=["Santé & Info"])
def health():
    return {"status": "ok"}
