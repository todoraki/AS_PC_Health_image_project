# LeafGuard

**Plant Disease Detection Platform for Acacia Senegal (AS) & Prosopis Cineraria (PC)**

> Software Architecture Project — Vighnesh PM (2025H1120159)

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

---

## Project Structure

```
leafguard/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   └── settings.py              # Paths, field names, DEMO_MODE flag
│   │   ├── models/
│   │   │   ├── species_classifier/      # CNN species model
│   │   │   ├── as_disease/              # AS hybrid CNN+SVM models
│   │   │   └── pc_disease/              # PC hybrid CNN+SVM models
│   │   ├── pipeline/
│   │   │   ├── base.py                  # BaseFilter interface
│   │   │   ├── preprocess.py            # Filter 1
│   │   │   ├── metadata_processor.py    # Filter 2
│   │   │   ├── feature_combiner.py      # Filter 3
│   │   │   ├── species_classifier.py    # Filter 4
│   │   │   ├── disease_classifier.py    # Filter 5
│   │   │   ├── result_formatter.py      # Filter 6
│   │   │   └── pipeline_runner.py       # Chain executor
│   │   ├── routes/
│   │   │   └── predict.py               # POST /api/predict endpoint
│   │   ├── services/
│   │   │   └── prediction_service.py
│   │   └── utils/
│   │       ├── image_utils.py
│   │       └── metadata_utils.py
│   └── tests/
│       └── test_pipeline.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── MetadataForm.jsx         # 10-field form with binary dropdowns
│   │   │   └── ResultDisplay.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   └── services/
│   │       └── api.js
│   └── vite.config.js
├── docs/
│   └── architecture.md
├── requirements.txt
└── README.md
```

---

## Author

**Vighnesh PM** — 2025H1120159  
Software Architecture, 2025


---

## What it does

1. User uploads a **leaf image** + **10 metadata measurements**.
2. The system classifies the **species** (Acacia Senegal or Prosopis Cineraria).
3. It then predicts whether the leaf is **Healthy** or **Unhealthy**.

---

## Architecture

| Level | Style |
|-------|-------|
| System | **Layered Architecture** (Presentation → Application → Domain → Infrastructure) |
| ML Pipeline | **Pipe-and-Filter** (6 independent stages chained together) |

See [`docs/architecture.md`](docs/architecture.md) for detailed diagrams and
quality-attribute mapping.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**

### 1. Backend

```bash
cd leafguard

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
cd backend
uvicorn app.main:app --reload --port 8000
```

The API is now running at **http://localhost:8000**.  
Swagger docs: **http://localhost:8000/docs**

### 2. Frontend

```bash
# In a new terminal
cd leafguard/frontend

npm install
npm run dev
```

The website is now at **http://localhost:5173**.

### 3. Run tests

```bash
cd leafguard/backend
python -m pytest tests/ -v
```

---

## Adding your trained models

1. Download the `.pkl` files from your remote server.
2. Copy them into `backend/app/models/`:

   | File | Purpose |
   |------|---------|
   | `species_classifier.pkl` | Classifies AS vs PC |
   | `as_disease_model.pkl` | Healthy/Unhealthy for Acacia Senegal |
   | `pc_disease_model.pkl` | Healthy/Unhealthy for Prosopis Cineraria |

3. Start the backend with **demo mode disabled**:

   ```bash
   DEMO_MODE=false uvicorn app.main:app --reload --port 8000
   ```

4. The pipeline will auto-load the models via `joblib`.

> **Note:** If your models expect a different feature vector format,
> edit `backend/app/pipeline/feature_combiner.py` and the relevant
> classifier filter. See `backend/app/models/README.md` for details.

---

## Metadata Fields (10 data points per leaf)

| # | Field | Unit / Range |
|---|-------|-------------|
| 1 | Leaf Length | 0.5 – 30 cm |
| 2 | Leaf Width | 0.2 – 15 cm |
| 3 | Leaf Area | 0.1 – 200 cm² |
| 4 | Number of Spots | 0 – 50 |
| 5 | Spot Coverage | 0 – 100 % |
| 6 | Yellowing | 0 – 100 % |
| 7 | Wilting Score | 1 – 10 |
| 8 | Moisture Level | 1 – 10 |
| 9 | Texture Score | 1 – 10 |
| 10 | Edge Damage Score | 1 – 10 |

---

## Project Structure

```
leafguard/
├── frontend/                 # Presentation Layer (React + Vite)
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page-level views
│   │   └── services/         # API client
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # Application + Domain + Infrastructure
│   ├── app/
│   │   ├── config/           # Settings & constants
│   │   ├── utils/            # Image & metadata helpers
│   │   ├── pipeline/         # Pipe-and-Filter stages
│   │   ├── services/         # Business logic
│   │   ├── routes/           # FastAPI endpoints
│   │   ├── models/           # .pkl model files (add here)
│   │   └── main.py           # FastAPI entry point
│   └── tests/                # pytest tests
│
├── data/                     # Sample test images
├── docs/                     # Architecture documentation
├── requirements.txt
└── README.md
```

---

## Execution Order (Step-by-step)

| Step | What | Command |
|------|------|---------|
| 1 | Install Python deps | `pip install -r requirements.txt` |
| 2 | Run backend tests | `cd backend && python -m pytest tests/ -v` |
| 3 | Start backend | `cd backend && uvicorn app.main:app --reload` |
| 4 | Test API with Swagger | Open `http://localhost:8000/docs` |
| 5 | Install frontend deps | `cd frontend && npm install` |
| 6 | Start frontend | `npm run dev` |
| 7 | Open website | `http://localhost:5173` |
| 8 | Add real models | Copy `.pkl` → `backend/app/models/`, restart with `DEMO_MODE=false` |
