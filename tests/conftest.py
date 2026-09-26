import sys
from pathlib import Path

# Ajouter la racine du projet au sys.path afin que les imports `backend.*` soient résolus
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
