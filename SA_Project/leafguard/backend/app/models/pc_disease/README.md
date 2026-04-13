# PC Disease Model — Prosopis Cineraria

## Status: Waiting for model files

When your PC disease model is ready, place the same four files here:

| File Name                  | What it is |
| -------------------------- | ---------- |
| `new_cnn_svm_cnn.h5`       | CNN feature extractor for PC leaves |
| `hybrid_cnn_tab_svm.pkl`   | Final SVM classifier for PC |
| `cnn_scaler.pkl`           | `StandardScaler` for CNN embeddings |
| `tabular_scaler.pkl`       | `StandardScaler` for the Week column |

The pipeline uses the **same hybrid CNN+SVM architecture** as the AS disease model.
The tabular feature vector layout is identical (see `as_disease/README.md`).

Once you add the files and `DEMO_MODE=false`, the pipeline will automatically use them.
