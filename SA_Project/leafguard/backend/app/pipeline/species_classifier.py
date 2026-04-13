import numpy as np
from app.pipeline.base import BaseFilter
from app.config.settings import SPECIES_CNN_MODEL_PATH, DEMO_MODE

# ── Keras 3.x / TF 2.16+ compatible import ──────────────────────
try:
    import keras
    _keras_load = keras.models.load_model
    _KERAS_AVAILABLE = True
except ImportError:
    try:
        from tensorflow.keras.models import load_model as _keras_load
        _KERAS_AVAILABLE = True
    except ImportError:
        _KERAS_AVAILABLE = False


class SpeciesClassifier(BaseFilter):
    """Filter 4 – Species Classification (AS / PC).

    Uses a CNN (pc_as_classifier_final.h5, Keras 3.x) to predict
    whether the leaf belongs to Acacia Senegal (AS) or
    Prosopis Cineraria (PC) from the grayscale image.

    Label convention (matches training):
        output < 0.5  → AS (class 0)
        output >= 0.5 → PC (class 1)
    For softmax output, argmax is used instead.

    In demo mode (no model file / Keras unavailable) a simple
    heuristic is used.

    Reads:  data["grayscale_cnn_input"], data["validated_metadata"]
    Writes: data["species"], data["species_confidence"]
    """

    def __init__(self):
        self.model = None
        if _KERAS_AVAILABLE and not DEMO_MODE and SPECIES_CNN_MODEL_PATH.exists():
            self.model = _keras_load(str(SPECIES_CNN_MODEL_PATH))

    def process(self, data: dict) -> dict:
        if self.model is not None:
            grayscale_input = data["grayscale_cnn_input"]  # (1, 224, 224, 1)
            output = self.model.predict(grayscale_input, verbose=0)

            # Handle both sigmoid (shape (1,1) or (1,)) and softmax (1, 2)
            output = output.flatten()
            if len(output) == 1:
                # Binary sigmoid
                prob_pc = float(output[0])
                prob_as = 1.0 - prob_pc
                if prob_pc >= 0.5:
                    species, confidence = "PC", prob_pc
                else:
                    species, confidence = "AS", prob_as
            else:
                # Softmax — index 0 = AS, index 1 = PC
                idx = int(np.argmax(output))
                confidence = float(output[idx])
                species = "AS" if idx == 0 else "PC"
        else:
            # ── Demo heuristic ──────────────────────────────────
            meta = data.get("validated_metadata", {})
            week         = float(meta.get("Week", 26))
            drought      = float(meta.get("Drought", 0))
            heat_drought = float(meta.get("Heat_Drought", 0))

            as_score = (1 - week / 52) * 0.5 + drought * 0.3 + heat_drought * 0.2
            if as_score >= 0.4:
                species, confidence = "AS", round(0.65 + as_score * 0.25, 4)
            else:
                species, confidence = "PC", round(0.70 + (1 - as_score) * 0.20, 4)

        data["species"] = species
        data["species_confidence"] = round(confidence, 4)
        return data
