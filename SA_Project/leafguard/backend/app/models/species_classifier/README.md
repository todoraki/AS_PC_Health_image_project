# Species Classifier Model

## Purpose
Classifies a leaf as either **AS** (Acacia Senegal) or **PC** (Prosopis Cineraria).

## Files to place here

| File Name                 | Description |
| ------------------------- | ----------- |
| `species_classifier.pkl`  | Trained scikit-learn classifier (loaded with `joblib`) |

## How to activate
1. Copy `species_classifier.pkl` into this folder.
2. Set `DEMO_MODE=false` when starting the backend.

## Model interface expected
- **`model.predict(X)`** — `X` is shape `(1, n_features)`.  
  Returns `"AS"` or `"PC"` (or `0` / `1` which the pipeline re-maps).
- **`model.predict_proba(X)`** (optional) — class probabilities for confidence score.
