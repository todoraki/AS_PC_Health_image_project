# LeafGuard – Architecture Documentation

## 1. Overview

LeafGuard is a plant disease detection platform for **Acacia Senegal (AS)** and
**Prosopis Cineraria (PC)**.  A user uploads a leaf image together with 9
morphological / visual metadata measurements.  The system first classifies the
species (AS or PC) and then predicts whether the leaf is **Healthy** or
**Unhealthy**.

---

## 2. Architectural Styles

### 2.1 System Level – Layered Architecture

The project is split into four logical layers:

```
┌───────────────────────────────────────────┐
│          Presentation Layer               │  React (Vite)
│   components / pages / services/api.js    │
├───────────────────────────────────────────┤
│          Application Layer                │  FastAPI routes
│   routes/predict.py                       │
├───────────────────────────────────────────┤
│          Domain / Business Layer          │  Services + Pipeline
│   services/prediction_service.py          │
│   pipeline/*  (Pipe-and-Filter)           │
├───────────────────────────────────────────┤
│          Infrastructure Layer             │  Model loading,
│   config/settings.py                      │  image/metadata utils,
│   utils/*   models/*.pkl                  │  file I/O
└───────────────────────────────────────────┘
```

Each layer only depends on the layer directly below it, ensuring **separation
of concerns** and **modifiability**.

### 2.2 ML Subsystem – Pipe-and-Filter

The core inference workflow is modelled as six independent **filters** connected
by a data dictionary (the "pipe"):

```
Image + Metadata
       │
       ▼
┌─────────────────────┐
│ 1. ImagePreprocessor │  Resize, normalize, flatten
└────────┬────────────┘
         │
┌────────▼────────────┐
│ 2. MetadataProcessor │  Validate, normalize 10 fields
└────────┬────────────┘
         │
┌────────▼────────────┐
│ 3. FeatureCombiner   │  Concatenate feature vectors
└────────┬────────────┘
         │
┌────────▼────────────┐
│ 4. SpeciesClassifier │  Predict AS or PC
└────────┬────────────┘
         │
┌────────▼────────────┐
│ 5. DiseaseClassifier │  Route model → Healthy/Unhealthy
└────────┬────────────┘
         │
┌────────▼────────────┐
│ 6. ResultFormatter   │  Build JSON response
└─────────────────────┘
```

Each filter extends `BaseFilter` and implements `process(data) → data`.  Filters
can be **replaced, reordered, or tested independently** without affecting the
rest of the pipeline.

---

## 3. Quality Attributes

| Attribute       | How it is achieved |
|-----------------|--------------------|
| **Modifiability**   | Pipe-and-Filter – swap any stage without touching others |
| **Maintainability** | Layered architecture – clear responsibility boundaries |
| **Scalability**     | Stateless API – can be horizontally scaled behind a load balancer |
| **Testability**     | Each filter is unit-testable; integration test covers the full pipeline |
| **Extensibility**   | New filters (e.g., a severity grader) can be inserted into the pipeline |

---

## 4. Data Flow

```
User (browser)
   │  POST /api/predict  (multipart: image + metadata JSON)
   ▼
FastAPI Route  →  PredictionService  →  PipelineRunner
                                           │
                                    Filters 1 → 6
                                           │
                                    Result JSON
   ◄──────────────────────────────────────┘
```

---

## 5. Technology Stack

| Component    | Technology |
|-------------|------------|
| Frontend    | React 18, Vite |
| Backend     | Python 3.10+, FastAPI, Uvicorn |
| ML Models   | scikit-learn (`.pkl` via joblib) |
| Image Proc. | Pillow, NumPy |

---

## 6. Folder Map

```
leafguard/
├── frontend/          # Presentation Layer
├── backend/
│   └── app/
│       ├── config/    # Infrastructure: settings
│       ├── utils/     # Infrastructure: image & metadata helpers
│       ├── pipeline/  # Domain: Pipe-and-Filter filters
│       ├── services/  # Domain: business logic
│       ├── routes/    # Application: API endpoints
│       ├── models/    # Infrastructure: ML model files
│       └── main.py    # Application: FastAPI entry point
├── data/              # Test images
├── docs/              # This file
├── requirements.txt
└── README.md
```
