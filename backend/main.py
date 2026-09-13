"""
AgroShield Mesh - Production FastAPI Application Entrypoint
"""

import time
from uuid import uuid4
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.core.config import settings
from backend.app.api.endpoints import router as api_router
from backend.app.db import init_db

# Initialize database schema
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=(
        "Production-grade agricultural intelligence platform combining field IoT telemetry, "
        "satellite NDVI observations, deterministic agronomic risk calculation, "
        "agricultural RAG with TNAU/ICAR citations, bounded agent workflow, and an Expert Review Gate."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_and_tracing_headers(request: Request, call_next):
    """Adds correlation request ID, processing timer, and security headers."""
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(process_time)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.exception_handler(Exception)
async def safe_exception_handler(request: Request, exc: Exception):
    """Sanitizes unhandled exceptions to prevent stack trace leaks in production."""
    req_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing the agronomic request.",
            "request_id": req_id
        }
    )


# Mount API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

import os
from fastapi.staticfiles import StaticFiles
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/dashboard", StaticFiles(directory=frontend_dist, html=True), name="dashboard")


@app.get("/", tags=["Root"])
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "operational",
        "docs": "/docs",
        "dashboard": "/dashboard/",
        "api_v1": settings.API_V1_STR
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
