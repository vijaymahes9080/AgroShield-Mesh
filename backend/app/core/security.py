"""
AgroShield Mesh - Security, Authentication, RBAC, and Audit Hashing
"""

import os
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
import jwt
import bcrypt
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.schemas.domain import UserRole

SECRET_KEY = os.getenv("SECRET_KEY", "agroshield-mesh-secure-production-secret-key-2026-xyz-unhackable")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security_scheme = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generates bcrypt hash for password."""
    # Ensure password within 72 bytes limit for bcrypt
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodes and validates a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature")


def get_current_user_payload(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme)) -> Dict[str, Any]:
    """Extracts authenticated user payload from bearer token or returns default demo user if unauthenticated."""
    if credentials is None:
        # Default fallback for demo / mock dashboard interactions
        return {
            "sub": "demo-farmer-id-1",
            "username": "vijay_farmer",
            "role": UserRole.ADMIN.value,  # Allow full local inspection in demo mode
            "farmer_id": "farmer-erode-01"
        }
    token = credentials.credentials
    return decode_access_token(token)


def require_roles(allowed_roles: List[UserRole]):
    """Role-based access control dependency."""
    def role_checker(payload: Dict[str, Any] = Depends(get_current_user_payload)) -> Dict[str, Any]:
        user_role = payload.get("role", UserRole.FARMER.value)
        if user_role not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required role in {[r.value for r in allowed_roles]}, current: {user_role}"
            )
        return payload
    return role_checker


def compute_sha256_hash(data_str: str) -> str:
    """Computes SHA-256 hash for audit events."""
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


def verify_hmac_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verifies HMAC-SHA256 signature for webhooks."""
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
