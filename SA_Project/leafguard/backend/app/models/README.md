# Models Directory

Three subfolders, one per model component:

| Folder                | What goes inside |
| --------------------- | ---------------- |
| `species_classifier/` | Classifies leaf as **AS** or **PC** |
| `as_disease/`         | Hybrid CNN+SVM — Healthy / Unhealthy for **Acacia Senegal** |
| `pc_disease/`         | Same hybrid architecture for **Prosopis Cineraria** (coming later) |

See each subfolder's `README.md` for exact file names and placement steps.

## How to add models

1. Download / copy the `.pkl` files from your remote server.
2. Place them in this folder (`backend/app/models/`).
3. Set the environment variable `DEMO_MODE=false` before starting the backend:
   ```bash
   DEMO_MODE=false uvicorn app.main:app --reload
   ```
4. The pipeline will automatically load the models at startup.

## Expected Model Interface

Each model is loaded with `joblib.load()` and must support:

- **`model.predict(X)`** – `X` is a 2-D numpy array of shape `(1, num_features)`.
  Returns a single prediction label.
- **`model.predict_proba(X)`** (optional) – returns class probabilities for
  confidence scores. If not available the system falls back to a default
  confidence value.

### Feature vector layout

The combined feature vector passed to each model is:

```
[ ...flattened_image_pixels (224×224×3 = 150528 floats)...,
  leaf_length_cm_norm, leaf_width_cm_norm, leaf_area_cm2_norm,
  num_spots_norm, spot_coverage_pct_norm, yellowing_pct_norm,
  wilting_score_norm, moisture_level_norm, texture_score_norm,
  edge_damage_score_norm ]
```

Total length: **150 538** (150 528 image + 10 metadata).

> **Note:** If your models expect a different feature layout, edit
> `backend/app/pipeline/feature_combiner.py` to match.
