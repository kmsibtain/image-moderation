from fastapi import APIRouter, Depends, HTTPException, status
from services.database import get_tokens_collection, get_usages_collection
from models.token import Token
from models.usage import Usage
from utils.auth import get_admin_token, get_current_token
import uuid
from datetime import datetime
from pymongo.collection import Collection

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/tokens", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_token(
    is_admin: bool = False, 
    admin_token: Token = Depends(get_admin_token),
    tokens_collection: Collection = Depends(get_tokens_collection)
):
    new_token_string = str(uuid.uuid4())
    new_token = Token(token=new_token_string, is_admin=is_admin, created_at=datetime.utcnow())
    
    # Run synchronous operation in executor
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: tokens_collection.insert_one(new_token.dict(by_alias=True))
    )
    return new_token

@router.get("/tokens", response_model=list[Token])
async def get_all_tokens(
    admin_token: Token = Depends(get_admin_token),
    tokens_collection: Collection = Depends(get_tokens_collection)
):
    import asyncio
    loop = asyncio.get_event_loop()
    
    # Get all tokens using executor
    def get_tokens():
        tokens = []
        for token in tokens_collection.find():
            tokens.append(Token(**token))
        return tokens
    
    tokens = await loop.run_in_executor(None, get_tokens)
    return tokens

@router.delete("/tokens/{token_string}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(
    token_string: str, 
    admin_token: Token = Depends(get_admin_token),
    tokens_collection: Collection = Depends(get_tokens_collection)
):
    import asyncio
    loop = asyncio.get_event_loop()
    
    result = await loop.run_in_executor(
        None,
        lambda: tokens_collection.delete_one({"token": token_string})
    )
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    return