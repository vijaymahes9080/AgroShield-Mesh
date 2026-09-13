"""
AgroShield Mesh - Core Settings & Configuration
"""

import os
from typing import List


class Settings:
    PROJECT_NAME: str = "AgroShield Mesh"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "agroshield-mesh-secure-production-secret-key-2026-xyz-unhackable")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # CORS Allowlist
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://agroshield-mesh.local"
    ]

    # Rate limiting thresholds (requests per minute)
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agroshield.db")

    # Coordinate Reference System
    DEFAULT_CRS: str = "EPSG:4326"


settings = Settings()
