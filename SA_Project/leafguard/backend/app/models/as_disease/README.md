# AS Disease Model — Acacia Senegal

## Architecture: Hybrid CNN + Tabular SVM

The model uses two inputs:
1. **Leaf image** — 224×224 grayscale → CNN extracts a 512-dim embedding
2. **Tabular metadata** — 10 fields (binary Yes/No + scaled Week)

These are combined → fed to an SVM for final Healthy / Unhealthy prediction.

---

## Files to place in THIS folder

> **You told me you already downloaded these. Copy them here:**
> `backend/app/models/as_disease/`

| File Name                  | What it is |
| -------------------------- | ---------- |
| `new_cnn_svm_cnn.h5`       | CNN feature extractor — outputs 512-dim embeddings |
| `hybrid_cnn_tab_svm.pkl`   | Final SVM classifier (loaded with `joblib`) |
| `cnn_scaler.pkl`           | `StandardScaler` fitted on CNN embeddings — scale before SVM |
| `tabular_scaler.pkl`       | `StandardScaler` fitted on the **Week** column only |

---

## Tabular feature vector layout (order matters for SVM)

| Index | Field            | Encoding |
| ----- | -----------------| -------- |
| 0     | Artefacts        | 0.0 / 1.0 |
| 1     | Control          | 0.0 / 1.0 |
| 2     | Heat             | 0.0 / 1.0 |
| 3     | Drought          | 0.0 / 1.0 |
| 4     | Heat_Drought     | 0.0 / 1.0 |
| 5     | Decolourization  | 0.0 / 1.0 |
| 6     | Spots            | 0.0 / 1.0 |
| 7     | Damage           | 0.0 / 1.0 (0 if unknown/missing) |
| 8     | Damage_missing   | 1.0 if Damage was not observed, else 0.0 |
| 9     | Week             | Scaled by `tabular_scaler.pkl` |

Combined SVM input: `[512 CNN embedding values, 10 tabular values]` = **522 features**

---

## How to activate
1. Copy all four files into this folder.
2. Install TensorFlow: `pip install tensorflow` (or `pip install tensorflow-cpu`).
3. Start the backend with `DEMO_MODE=false`:
   ```bash
   DEMO_MODE=false uvicorn app.main:app --reload --port 8000
   ```

The pipeline auto-detects and loads the models at startup.
