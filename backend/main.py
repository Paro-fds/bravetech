"""Point d'entrée de l'application FastAPI — FDS Portail.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import api_v1_router


# Sans cette configuration, uvicorn n'affiche pas les messages INFO de l'application : en mode console
# (sans RESEND_API_KEY), l'email de confirmation serait « envoyé » dans le vide.
logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")

# Le schéma de la base n'est plus créé ici : `python -m backend.scripts.migrer` l'applique avant l'API (US-023).

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
