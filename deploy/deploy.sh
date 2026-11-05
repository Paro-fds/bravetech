#!/usr/bin/env bash
# Déploiement du portail sur la VM de la FDS (US-026).
#
# Usage : deploy.sh <commit>   (40 caractères hexadécimaux, le commit de master dont les images sont sur GHCR)
#
# Appelé par GitHub Actions avec une clé SSH dédiée, limitée à ce script dans ~/.ssh/authorized_keys :
#   command="/home/devops/deploiement/deploy.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 …
# Le commit arrive alors dans SSH_ORIGINAL_COMMAND. Retour manuel à une version : même commande, avec ce commit.
#
# Étapes : télécharger le compose et les images du commit ; copier la base ; relancer ; vérifier /api/v1/sante ;
# en cas d'échec, revenir à la version précédente. Le script est installé hors du clone git (~/deploiement/),
# pour qu'une mise à jour du dépôt ne le modifie pas en pleine exécution.

set -euo pipefail

DOSSIER="${DOSSIER_PORTAIL:-$HOME/bravetech}"
SAUVEGARDES="${DOSSIER_SAUVEGARDES:-$HOME/sauvegardes/deploiements}"
COPIES_GARDEES=10
DEPOT_BRUT="https://raw.githubusercontent.com/Paro-fds/bravetech"
DELAI_SANTE=90

journal() { printf '[deploiement %s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

TAG="${1:-${SSH_ORIGINAL_COMMAND:-}}"
if [[ ! "$TAG" =~ ^[0-9a-f]{40}$ ]]; then
  journal "Refusé : un commit complet (40 caractères hexadécimaux) est attendu."
  exit 2
fi

cd "$DOSSIER"
exec 9>.deploiement.lock
flock -n 9 || { journal "Un autre déploiement est en cours."; exit 3; }

PORT="$(sed -n 's/^PORT=//p' .env | tail -n 1)"
PORT="${PORT:-80}"
PRECEDENT="$(cat .version-deployee 2>/dev/null || true)"

compose() { docker compose -f docker-compose.prod.yml "$@"; }

portail_repond() {
  local fin=$((SECONDS + DELAI_SANTE))
  while (( SECONDS < fin )); do
    if curl -fsS -o /dev/null "http://localhost:${PORT}/api/v1/sante"; then
      return 0
    fi
    sleep 3
  done
  return 1
}

journal "Version demandée : ${TAG} ; en ligne : ${PRECEDENT:-aucune (premier déploiement automatique)}."

# 1. Compose de ce commit, à côté de l'actuel (gardé pour le retour arrière)
curl -fsSL "${DEPOT_BRUT}/${TAG}/docker-compose.prod.yml" -o docker-compose.prod.yml.nouveau
[[ -f docker-compose.prod.yml ]] && cp docker-compose.prod.yml docker-compose.prod.yml.precedent

# 2. Images : si elles manquent, on s'arrête avant d'avoir touché au portail
mv docker-compose.prod.yml.nouveau docker-compose.prod.yml
if ! TAG="$TAG" compose pull --quiet; then
  journal "ÉCHEC : images introuvables sur GHCR pour ${TAG}. Rien n'a été changé."
  [[ -f docker-compose.prod.yml.precedent ]] && mv docker-compose.prod.yml.precedent docker-compose.prod.yml
  exit 1
fi

# 3. Copie de la base avant la mise à jour (une migration peut la modifier) ; on garde les dernières
mkdir -p "$SAUVEGARDES"
chmod 700 "$SAUVEGARDES"
if docker ps --filter "label=com.docker.compose.project=bravetech" --filter "label=com.docker.compose.service=db" -q | grep -q .; then
  COPIE="${SAUVEGARDES}/avant-${TAG:0:7}-$(date -u +%Y%m%dT%H%M%SZ).dump"
  TAG="$TAG" compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$COPIE"
  chmod 600 "$COPIE"
  journal "Copie de la base : ${COPIE} ($(du -h "$COPIE" | cut -f1))."
  ls -1t "$SAUVEGARDES"/avant-*.dump | tail -n +$((COPIES_GARDEES + 1)) | xargs -r rm -f
else
  journal "Pas de base en marche : aucune copie (premier lancement)."
fi

# 4. Relance avec les nouvelles images (les migrations s'appliquent au démarrage du backend)
TAG="$TAG" compose up -d --remove-orphans

# 5. Santé : le portail répond-il, base comprise ?
if portail_repond; then
  echo "$TAG" > .version-deployee
  journal "SUCCÈS : ${TAG} est en ligne."
  exit 0
fi

journal "ÉCHEC : /api/v1/sante ne répond pas après ${DELAI_SANTE} s. Journaux du backend :"
TAG="$TAG" compose logs --tail 30 backend || true

if [[ -z "$PRECEDENT" || ! -f docker-compose.prod.yml.precedent ]]; then
  journal "Aucune version précédente connue : retour arrière impossible, intervention manuelle nécessaire."
  exit 1
fi

journal "Retour à la version précédente : ${PRECEDENT}."
mv docker-compose.prod.yml.precedent docker-compose.prod.yml
TAG="$PRECEDENT" compose up -d --remove-orphans
if portail_repond; then
  journal "Retour arrière réussi : ${PRECEDENT} est en ligne. Le déploiement de ${TAG} a échoué."
else
  journal "Retour arrière sans réponse de santé : intervention manuelle nécessaire. Copie de la base : ${COPIE:-aucune}."
fi
exit 1
