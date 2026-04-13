import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.prediction_service import predict, get_pipeline_info

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/predict")
async def predict_disease(
    image: UploadFile = File(..., description="Leaf image (JPEG/PNG)"),
    metadata: str = Form(..., description="JSON string of 10 metadata fields"),
):
    """Upload a leaf image and metadata; receive species + health prediction."""

    # ── Validate file type ───────────────────────────────
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, or WebP images are accepted.",
        )

    # ── Read and validate image bytes ────────────────────
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image file.")
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image too large (max 10 MB).")

    # ── Parse metadata JSON ──────────────────────────────
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata JSON.")

    # ── Run prediction pipeline ──────────────────────────
    try:
        result = predict(image_bytes, metadata_dict)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    return {"status": "success", "data": result}


@router.get("/pipeline-info")
async def pipeline_info():
    """Return the names and count of pipeline stages (useful for docs/debug)."""
    return get_pipeline_info()
