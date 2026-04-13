"""Tests for the Pipe-and-Filter pipeline (demo mode)."""

import io
import numpy as np
from PIL import Image

from app.pipeline import create_pipeline
from app.pipeline.preprocess import ImagePreprocessor
from app.pipeline.metadata_processor import MetadataPreprocessor
from app.pipeline.feature_combiner import FeatureCombiner
from app.utils.metadata_utils import validate_and_encode_metadata, encode_to_array


# ── Helpers ──────────────────────────────────────────────────────
def _make_test_image_bytes() -> bytes:
    """Generate a tiny in-memory JPEG for testing."""
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


# 10 tabular fields matching the actual Excel sheet columns
SAMPLE_METADATA = {
    "Artefacts":       "no",
    "Control":         "yes",
    "Heat":            "no",
    "Drought":         "yes",
    "Heat_Drought":    "no",
    "Decolourization": "no",
    "Spots":           "yes",
    "Damage":          "unknown",   # triggers Damage_missing = 1
    "Week":            14,
}

# Expected encoded form (Damage=0, Damage_missing=1 for "unknown")
ENCODED_METADATA = {
    "Artefacts":       0.0,
    "Control":         1.0,
    "Heat":            0.0,
    "Drought":         1.0,
    "Heat_Drought":    0.0,
    "Decolourization": 0.0,
    "Spots":           1.0,
    "Damage":          0.0,
    "Damage_missing":  1.0,
    "Week":            14.0,
}


# ── Unit Tests ───────────────────────────────────────────────────
def test_validate_encode_metadata_accepts_valid():
    result = validate_and_encode_metadata(SAMPLE_METADATA)
    assert len(result) == 10
    assert result["Damage_missing"] == 1.0
    assert result["Damage"] == 0.0
    assert result["Week"] == 14.0


def test_validate_metadata_rejects_missing_field():
    bad = {k: v for k, v in SAMPLE_METADATA.items() if k != "Spots"}
    try:
        validate_and_encode_metadata(bad)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_validate_metadata_rejects_invalid_binary():
    bad = {**SAMPLE_METADATA, "Heat": "maybe"}
    try:
        validate_and_encode_metadata(bad)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_encode_to_array_shape():
    arr = encode_to_array(ENCODED_METADATA)
    assert arr.shape == (10,)
    assert arr.dtype == np.float32


def test_image_preprocessor_outputs():
    data = {"image_bytes": _make_test_image_bytes()}
    result = ImagePreprocessor().process(data)
    assert "grayscale_cnn_input" in result
    assert result["grayscale_cnn_input"].shape == (1, 224, 224, 1)
    assert result["grayscale_cnn_input"].min() >= 0.0
    assert result["grayscale_cnn_input"].max() <= 1.0


def test_metadata_preprocessor():
    data = {"metadata": SAMPLE_METADATA}
    result = MetadataPreprocessor().process(data)
    assert "metadata_features" in result
    assert result["metadata_features"].shape == (10,)
    assert result["metadata_features"][8] == 1.0  # Damage_missing


def test_feature_combiner_passthrough():
    meta_features = np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 14.0], dtype=np.float32)
    data = {"metadata_features": meta_features}
    result = FeatureCombiner().process(data)
    assert result["combined_features"].shape == (10,)
    np.testing.assert_array_equal(result["combined_features"], meta_features)


# ── Integration Test (full pipeline, demo mode) ─────────────────
def test_full_pipeline_demo_mode():
    pipeline = create_pipeline()
    data = {
        "image_bytes": _make_test_image_bytes(),
        "metadata": SAMPLE_METADATA,
    }
    result = pipeline.run(data)

    assert "result" in result
    res = result["result"]
    assert res["species"]["code"] in ("AS", "PC")
    assert res["health"]["status"] in ("Healthy", "Unhealthy")
    assert 0.0 <= res["species"]["confidence"] <= 1.0
    assert 0.0 <= res["health"]["confidence"] <= 1.0
    assert len(res["summary"]) > 0

