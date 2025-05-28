from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.database import get_tokens_collection
from models.token import Token
import os
from pymongo.collection import Collection

security_scheme = HTTPBearer()

async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    tokens_collection: Collection = Depends(get_tokens_collection)
):
    """
    Dependency to validate the bearer token.
    """
    token_string = credentials.credentials
    
    # Run the synchronous MongoDB operation in an executor
    import asyncio
    loop = asyncio.get_event_loop()
    stored_token = await loop.run_in_executor(
        None, 
        lambda: tokens_collection.find_one({"token": token_string})
    )
    
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(**stored_token)

async def get_admin_token(current_token: Token = Depends(get_current_token)):
    """
    Dependency to ensure the current token has admin privileges.
    """
    if not current_token.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin privileges required.",
        )
    return current_token