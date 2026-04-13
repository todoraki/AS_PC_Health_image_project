# LeafGuard

**Plant Disease Detection Platform for Acacia Senegal (AS) & Prosopis Cineraria (PC)**

---

## Overview

LeafGuard is a full-stack web application that detects plant disease in two arid-zone tree species using a **hybrid CNN + SVM** machine learning pipeline. The user uploads a leaf image and fills in 10 metadata fields about environmental stress conditions. The system:

1. Classifies the **species** — Acacia Senegal (AS) or Prosopis Cineraria (PC)
2. Predicts whether the leaf is **Healthy or Unhealthy**
3. Returns confidence scores derived from the real model outputs

---

## Architecture

| Level | Style |
|---|---|
| System | **Layered Architecture** — Presentation → Application → Domain → Infrastructure |
| ML Subsystem | **Pipe-and-Filter** — 6 independent processing stages chained via a shared data dictionary |

### Pipe-and-Filter Pipeline (6 Stages)

```
[Image Upload + Metadata]
        │
        ▼
 Filter 1: ImagePreprocessor
   └─ Loads image, converts to grayscale (224×224), normalises to [0,1]
   └─ Output: grayscale_cnn_input shape (1, 224, 224, 1)
        │
        ▼
 Filter 2: MetadataProcessor
   └─ Validates & encodes 10 tabular fields
   └─ Output: metadata_features shape (10,)
        │
        ▼
 Filter 3: FeatureCombiner
   └─ Passthrough for disease models; prepares combined_features for species CNN
        │
        ▼
 Filter 4: SpeciesClassifier
   └─ CNN (pc_as_classifier_final.h5, Keras 3.x)
   └─ Sigmoid / softmax output → AS or PC + confidence
        │
        ▼
 Filter 5: DiseaseClassifier
   └─ Species-specific Hybrid CNN + SVM:
        CNN .h5  → 512-dim embedding
        cnn_scaler (AS only) → scaled embedding
        tabular_scaler → scaled Week feature
        Concat → 522-dim (AS) / 521-dim (PC) → SVM.predict()
   └─ Output: Healthy / Unhealthy + real confidence (decision_function distance)
        │
        ▼
 Filter 6: ResultFormatter
   └─ Assembles final JSON response
```

---

## Model Files

Model binaries are **not committed** to this repository (they exceed GitHub's 100 MB limit and contain sensitive trained weights). Place them in the correct subfolders before running in real-model mode.

```
backend/app/models/
├── species_classifier/
│   └── pc_as_classifier_final.h5       ← Keras 3.x CNN (binary sigmoid)
│
├── as_disease/
│   ├── new_cnn_svm_cnn.h5              ← CNN feature extractor (512-dim output)
│   ├── hybrid_cnn_tab_svm.pkl          ← SVM classifier (linear kernel)
│   ├── cnn_scaler.pkl                  ← StandardScaler for CNN embeddings
│   └── tabular_scaler.pkl              ← StandardScaler for Week feature
│
└── pc_disease/
    ├── pc_cnn_svm_cnn.h5               ← CNN feature extractor (512-dim output)
    ├── pc_hybrid_cnn_tab_svm.pkl       ← SVM classifier (linear kernel)
    └── tabular_scaler.pkl              ← StandardScaler for Week feature
                                           (no cnn_scaler for PC)
```

> **Note:** The species CNN and AS/PC disease models were saved with **Keras 3.x / TF 2.16+**. Ensure your environment meets this requirement.

---

## Metadata Fields (10 features)

| Field | Type | Description |
|---|---|---|
| Artefacts | Binary (0/1) | Image artefacts present |
| Control | Binary (0/1) | Control treatment |
| Heat | Binary (0/1) | Heat stress applied |
| Drought | Binary (0/1) | Drought stress applied |
| Heat_Drought | Binary (0/1) | Combined heat + drought stress |
| Decolourization | Binary (0/1) | Leaf discolouration observed |
| Spots | Binary (0/1) | Spots visible on leaf |
| Damage | Binary (0/1) | Physical damage present (0 if unknown) |
| Damage_missing | Binary (0/1) | 1 = Damage was not observed / unknown |
| Week | Integer (1–52) | Week of observation in the growing season |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.115 + Uvicorn |
| ML Runtime | TensorFlow / Keras 3.x, scikit-learn 1.8+ |
| Image Processing | Pillow, NumPy |
| Frontend | React 18 + Vite 6 |
| Language | Python 3.10+, JavaScript (ES2022) |

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**
- Trained model files (see [Model Files](#model-files) section above)

### 1. Create virtual environment & install dependencies

```bash
cd leafguard
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Place model files

Copy the model binaries into their respective folders under `backend/app/models/` as shown in the [Model Files](#model-files) section.

### 3. Start the backend

```bash
cd backend
DEMO_MODE=false python -m uvicorn app.main:app --reload --port 8000
```

> Set `DEMO_MODE=true` (or omit the variable) to run with heuristic predictions if model files are not available.

API is available at **http://localhost:8000**  
Swagger docs: **http://localhost:8000/docs**

### 4. Start the frontend

```bash
# In a separate terminal
cd leafguard/frontend
npm install
npm run dev
```

App is available at **http://localhost:5173**

### 5. Run tests

```bash
cd leafguard/backend
python -m pytest tests/ -v
```



