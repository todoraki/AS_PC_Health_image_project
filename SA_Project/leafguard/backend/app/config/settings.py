import os
from pathlib import Path

# ── Directory Paths ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# ── Species Classifier (CNN — Keras 3.x / TF 2.16+) ─────────────
SPECIES_CLASSIFIER_DIR = MODELS_DIR / "species_classifier"
SPECIES_CNN_MODEL_PATH = SPECIES_CLASSIFIER_DIR / "pc_as_classifier_final.h5"

# ── AS Disease Model (Hybrid CNN + SVM) ─────────────────────────
AS_DISEASE_DIR = MODELS_DIR / "as_disease"
AS_CNN_MODEL_PATH     = AS_DISEASE_DIR / "new_cnn_svm_cnn.h5"
AS_SVM_MODEL_PATH     = AS_DISEASE_DIR / "hybrid_cnn_tab_svm.pkl"
AS_CNN_SCALER_PATH    = AS_DISEASE_DIR / "cnn_scaler.pkl"
AS_TAB_SCALER_PATH    = AS_DISEASE_DIR / "tabular_scaler.pkl"

# ── PC Disease Model (Hybrid CNN + SVM, no CNN embedding scaler) ─
PC_DISEASE_DIR = MODELS_DIR / "pc_disease"
PC_CNN_MODEL_PATH     = PC_DISEASE_DIR / "pc_cnn_svm_cnn.h5"
PC_SVM_MODEL_PATH     = PC_DISEASE_DIR / "pc_hybrid_cnn_tab_svm.pkl"
PC_CNN_SCALER_PATH    = None   # not present for PC model
PC_TAB_SCALER_PATH    = PC_DISEASE_DIR / "tabular_scaler.pkl"

# ── Image Preprocessing ─────────────────────────────────────────
IMAGE_SIZE = (224, 224)       # Width × Height fed to the CNN
IMAGE_CHANNELS = 1            # CNN takes grayscale (1 channel)

# ── Metadata / Tabular Field Definitions ────────────────────────
# These 10 fields come from the Excel metadata sheet.
# Binary fields (Yes → 1.0 / No → 0.0):
BINARY_FIELDS = [
    "Artefacts",
    "Control",
    "Heat",
    "Drought",
    "Heat_Drought",       # "Heat+Drought" renamed for safe key use
    "Decolourization",
    "Spots",
    "Damage",             # optional — user may mark as "unknown"
]
# Derived field (computed, not collected directly from user):
#   Damage_missing = 1.0 if Damage was marked unknown, else 0.0
# Numeric field:
NUMERIC_FIELDS = ["Week"]    # integer, 1-52

# All 10 tabular features in the exact order the SVM was trained on:
METADATA_FIELDS = [
    "Artefacts",
    "Control",
    "Heat",
    "Drought",
    "Heat_Drought",
    "Decolourization",
    "Spots",
    "Damage",
    "Damage_missing",
    "Week",
]

# ── CORS ─────────────────────────────────────────────────────────
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# ── Demo Mode ────────────────────────────────────────────────────
# When True, the system uses heuristic predictions instead of real models.
# Set env var DEMO_MODE=false once you have placed the model files.
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
