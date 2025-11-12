"""
Authentication utilities for Komfyrvakt.
Simple API key-based authentication.
"""

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import settings


security = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """
    Verify API key from Authorization header.
    
    Args:
        credentials: HTTP Bearer token credentials
    
    Returns:
        True if valid
    
    Raises:
        HTTPException: If API key is invalid
    """
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme. Use: Authorization: Bearer {api_key}"
        )
    
    if not settings.validate_api_key(credentials.credentials):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return True

