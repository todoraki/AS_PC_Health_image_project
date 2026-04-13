from app.pipeline import create_pipeline

# Singleton pipeline instance – created once and reused for every request.
_pipeline = create_pipeline()


def predict(image_bytes: bytes, metadata: dict) -> dict:
    """Run the full disease-detection pipeline.

    Parameters
    ----------
    image_bytes : bytes
        Raw bytes of the uploaded leaf image.
    metadata : dict
        Dictionary with 10 metadata fields (see config/settings.py).

    Returns
    -------
    dict
        Structured result with species and health predictions.
    """
    initial_data = {
        "image_bytes": image_bytes,
        "metadata": metadata,
    }
    result_data = _pipeline.run(initial_data)
    return result_data["result"]


def get_pipeline_info() -> dict:
    """Return information about the current pipeline stages."""
    return {
        "stages": _pipeline.get_stage_names(),
        "num_stages": len(_pipeline.get_stage_names()),
    }
