from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router
from app.config.settings import FRONTEND_URL

app = FastAPI(
    title="LeafGuard API",
    description=(
        "Plant Disease Detection Platform for "
        "Acacia Senegal & Prosopis Cineraria"
    ),
    version="1.0.0",
)

# ── CORS – allow the React dev server and common local origins ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount API routes ─────────────────────────────────────────────
app.include_router(predict_router, prefix="/api", tags=["prediction"])


@app.get("/")
def root():
    return {"message": "LeafGuard API is running", "version": "1.0.0"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
