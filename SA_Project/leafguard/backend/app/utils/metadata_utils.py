import numpy as np
from app.config.settings import METADATA_FIELDS, BINARY_FIELDS, NUMERIC_FIELDS

# Valid range for Week
WEEK_MIN, WEEK_MAX = 1, 52


def validate_and_encode_metadata(raw_metadata: dict) -> dict:
    """Validate all metadata fields and encode them for the SVM pipeline.

    Binary fields (Artefacts, Control, Heat, Drought, Heat_Drought,
    Decolourization, Spots, Damage) accept:
      - 1 / "1" / "yes" / "Yes" / "YES"  → 1.0
      - 0 / "0" / "no"  / "No"  / "NO"   → 0.0
      - "unknown" / "Unknown" / ""         → 0.0  (only valid for Damage)

    Damage_missing:
      - Pass explicitly as 0 or 1, OR
      - Omit it entirely — the backend auto-sets it to 1 if Damage was
        submitted as "unknown", otherwise 0.

    Week: integer between 1 and 52.

    Returns a validated dict with float values for every field in
    METADATA_FIELDS (10 entries), ready for numpy conversion.
    """
    encoded: dict = {}

    # ── Binary fields ────────────────────────────────────────────
    for field in BINARY_FIELDS:
        if field not in raw_metadata:
            raise ValueError(f"Missing required metadata field: '{field}'")

        raw = raw_metadata[field]

        # Handle Damage=unknown specially (sets Damage=0, Damage_missing=1)
        if field == "Damage" and str(raw).strip().lower() in ("unknown", ""):
            encoded["Damage"] = 0.0
            encoded["Damage_missing"] = 1.0
            continue

        encoded[field] = _parse_binary(field, raw)

    # ── Damage_missing (if not already set by Damage=unknown) ───
    if "Damage_missing" not in encoded:
        dm_raw = raw_metadata.get("Damage_missing", 0)
        encoded["Damage_missing"] = _parse_binary("Damage_missing", dm_raw)

    # ── Week ─────────────────────────────────────────────────────
    if "Week" not in raw_metadata:
        raise ValueError("Missing required metadata field: 'Week'")
    try:
        week = int(float(raw_metadata["Week"]))
    except (TypeError, ValueError):
        raise ValueError(f"'Week' must be an integer, got: {raw_metadata['Week']!r}")
    if not (WEEK_MIN <= week <= WEEK_MAX):
        raise ValueError(
            f"'Week' must be between {WEEK_MIN} and {WEEK_MAX}, got {week}"
        )
    encoded["Week"] = float(week)

    return encoded


def encode_to_array(encoded_metadata: dict) -> np.ndarray:
    """Convert an encoded metadata dict to a float32 numpy array.

    The order follows METADATA_FIELDS exactly — this must match the
    order used during SVM training.

    Note: 'Week' is still the raw integer float here.
    The DiseaseClassifier will apply tabular_scaler to index 9 (Week)
    just before calling the SVM.
    """
    return np.array(
        [encoded_metadata[field] for field in METADATA_FIELDS],
        dtype=np.float32,
    )


# ── keep old names as aliases so nothing else breaks ────────────
def validate_metadata(metadata: dict) -> dict:
    return validate_and_encode_metadata(metadata)


def normalize_metadata(metadata: dict) -> np.ndarray:
    return encode_to_array(metadata)


# ── Helpers ──────────────────────────────────────────────────────
def _parse_binary(field: str, raw) -> float:
    """Parse a binary field value to 0.0 or 1.0."""
    if isinstance(raw, (int, float)):
        v = float(raw)
        if v not in (0.0, 1.0):
            raise ValueError(
                f"Binary field '{field}' must be 0 or 1, got {raw!r}"
            )
        return v
    s = str(raw).strip().lower()
    if s in ("1", "yes", "true"):
        return 1.0
    if s in ("0", "no", "false"):
        return 0.0
    raise ValueError(
        f"Binary field '{field}' must be Yes/No or 0/1, got {raw!r}"
    )
