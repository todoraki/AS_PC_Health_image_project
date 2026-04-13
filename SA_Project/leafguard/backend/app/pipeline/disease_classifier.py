import joblib
import numpy as np
from app.pipeline.base import BaseFilter
from app.config.settings import (
    AS_CNN_MODEL_PATH,
    AS_SVM_MODEL_PATH,
    AS_CNN_SCALER_PATH,
    AS_TAB_SCALER_PATH,
    PC_CNN_MODEL_PATH,
    PC_SVM_MODEL_PATH,
    PC_CNN_SCALER_PATH,
    PC_TAB_SCALER_PATH,
    DEMO_MODE,
)

# ── Keras 3.x / TF 2.16+ compatible import ──────────────────────
try:
    import keras
    _keras_load = keras.models.load_model
    _TENSORFLOW_AVAILABLE = True
except ImportError:
    try:
        from tensorflow.keras.models import load_model as _keras_load
        _TENSORFLOW_AVAILABLE = True
    except ImportError:
        _TENSORFLOW_AVAILABLE = False


def _load_keras(path):
    """Load a Keras .h5 model; returns None if Keras unavailable or file missing."""
    if _TENSORFLOW_AVAILABLE and path is not None and path.exists():
        return _keras_load(str(path))
    return None


class DiseaseClassifier(BaseFilter):
    """Filter 5 – Disease / Health Classification.

    Architecture (when real models are present):
    ─────────────────────────────────────────────
    1. Grayscale CNN input  (1, 224, 224, 1)
          │
          ▼
    2. CNN feature extractor  → 512-dim embedding
          │
    3. cnn_scaler.transform() → scaled 512-dim embedding
          │
    4. Tabular features (10)  → tabular_scaler scales Week (index 9)
          │
    5. Concat → 522-dim vector → SVM.predict() → Healthy / Unhealthy

    Demo mode (no model files / TF not installed):
    ───────────────────────────────────────────────
    Uses a simple heuristic based on the tabular metadata fields.

    Reads:  data["species"], data["grayscale_cnn_input"],
            data["metadata_features"], data["validated_metadata"]
    Writes: data["health_status"], data["health_confidence"],
            data["disease_model_used"]
    """

    def __init__(self):
        # ── Load AS models ───────────────────────────────────────
        self.as_cnn = None
        self.as_svm = None
        self.as_cnn_scaler = None
        self.as_tab_scaler = None

        if not DEMO_MODE and _TENSORFLOW_AVAILABLE:
            self.as_cnn        = _load_keras(AS_CNN_MODEL_PATH)
            if AS_SVM_MODEL_PATH.exists():
                self.as_svm        = joblib.load(AS_SVM_MODEL_PATH)
            if AS_CNN_SCALER_PATH.exists():
                self.as_cnn_scaler = joblib.load(AS_CNN_SCALER_PATH)
            if AS_TAB_SCALER_PATH.exists():
                self.as_tab_scaler = joblib.load(AS_TAB_SCALER_PATH)

        # ── Load PC models (different filenames, no CNN embedding scaler) ──
        self.pc_cnn = None
        self.pc_svm = None
        self.pc_cnn_scaler = None   # intentionally absent for PC
        self.pc_tab_scaler = None

        if not DEMO_MODE and _TENSORFLOW_AVAILABLE:
            self.pc_cnn        = _load_keras(PC_CNN_MODEL_PATH)
            if PC_SVM_MODEL_PATH is not None and PC_SVM_MODEL_PATH.exists():
                self.pc_svm        = joblib.load(PC_SVM_MODEL_PATH)
            # PC_CNN_SCALER_PATH is None — skip silently
            if PC_CNN_SCALER_PATH is not None and PC_CNN_SCALER_PATH.exists():
                self.pc_cnn_scaler = joblib.load(PC_CNN_SCALER_PATH)
            if PC_TAB_SCALER_PATH is not None and PC_TAB_SCALER_PATH.exists():
                self.pc_tab_scaler = joblib.load(PC_TAB_SCALER_PATH)

    # ── Internal helpers ─────────────────────────────────────────
    def _models_ready(self, species: str) -> bool:
        """Return True only when the required model components are loaded."""
        if species == "AS":
            # AS requires all four: CNN, SVM, CNN scaler, tabular scaler
            return all([self.as_cnn, self.as_svm,
                        self.as_cnn_scaler, self.as_tab_scaler])
        # PC has no CNN embedding scaler — only three components needed
        return all([self.pc_cnn, self.pc_svm, self.pc_tab_scaler])

    def _select_models(self, species: str):
        if species == "AS":
            return self.as_cnn, self.as_svm, self.as_cnn_scaler, self.as_tab_scaler
        return self.pc_cnn, self.pc_svm, self.pc_cnn_scaler, self.pc_tab_scaler

    # ── Main filter ──────────────────────────────────────────────
    def process(self, data: dict) -> dict:
        species = data["species"]
        model_name = "as_disease" if species == "AS" else "pc_disease"

        if self._models_ready(species):
            health, confidence = self._real_inference(data, species)
        else:
            health, confidence = self._demo_heuristic(data)

        data["health_status"] = health
        data["health_confidence"] = confidence
        data["disease_model_used"] = model_name
        return data

    def _real_inference(self, data: dict, species: str):
        """Hybrid CNN + tabular SVM inference."""
        cnn_model, svm_model, cnn_scaler, tab_scaler = self._select_models(species)

        # 1. CNN → 512-dim embedding
        grayscale_input = data["grayscale_cnn_input"]  # (1, 224, 224, 1)
        embedding = cnn_model.predict(grayscale_input, verbose=0)[0]  # (512,)

        # 2. Scale CNN embedding (AS has cnn_scaler; PC uses raw embedding)
        if cnn_scaler is not None:
            emb_scaled = cnn_scaler.transform(embedding.reshape(1, -1))[0]
        else:
            emb_scaled = embedding

        # 3. Tabular features — scale Week (index 9) with tabular_scaler
        tab_features = data["metadata_features"].copy()           # (10,)
        week_scaled = tab_scaler.transform([[tab_features[9]]])[0][0]
        tab_features[9] = week_scaled                              # in-place replace

        # PC was trained without Damage_missing (index 8) → drop it for PC
        # AS: 512 + 10 = 522 features; PC: 512 + 9 = 521 features
        if species == "PC":
            tab_features = np.delete(tab_features, 8)             # remove index 8

        # 4. Concatenate → 522-dim (AS) or 521-dim (PC) SVM input
        combined = np.concatenate([emb_scaled, tab_features]).reshape(1, -1)

        # 5. SVM predict
        prediction = svm_model.predict(combined)[0]
        try:
            proba = svm_model.predict_proba(combined)[0]
            confidence = float(max(proba))
        except AttributeError:
            # probability=False — use decision_function distance mapped to [0.5, 1.0]
            # Larger absolute distance = higher certainty
            dist = float(abs(svm_model.decision_function(combined)[0]))
            confidence = round(min(0.50 + dist / (2.0 * (1.0 + dist)), 0.99), 4)

        # Normalise label
        health = str(prediction)
        if health not in ("Healthy", "Unhealthy"):
            health = "Healthy" if str(prediction) in ("0", "healthy") else "Unhealthy"

        return health, confidence

    def _demo_heuristic(self, data: dict) -> tuple:
        """Heuristic prediction used when model files are absent."""
        meta = data.get("validated_metadata", {})

        spots          = float(meta.get("Spots", 0))
        decolour       = float(meta.get("Decolourization", 0))
        damage         = float(meta.get("Damage", 0))
        damage_missing = float(meta.get("Damage_missing", 0))
        heat           = float(meta.get("Heat", 0))
        drought        = float(meta.get("Drought", 0))
        heat_drought   = float(meta.get("Heat_Drought", 0))

        score = (
            spots * 0.25
            + decolour * 0.25
            + damage * 0.15
            + heat * 0.10
            + drought * 0.10
            + heat_drought * 0.15
        )
        # damage_missing means we assume worst-case
        if damage_missing:
            score += 0.10

        if score >= 0.3:
            health = "Unhealthy"
            confidence = min(0.60 + score * 0.35, 0.95)
        else:
            health = "Healthy"
            confidence = min(0.70 + (1 - score) * 0.22, 0.95)

        return health, round(confidence, 4)
