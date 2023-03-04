from typing import Optional
from fastapi import Header, Depends, HTTPException
from db import User
from users import current_active_user
from schemas import UserCreate
import os

MASTER_KEY = os.getenv("MASTER_KEY")

async def check_master_key(master_key: str = Header(None)):
    if master_key != MASTER_KEY:
        raise HTTPException(status_code=401, detail="MASTER_KEY header is missing or wrong")
    
async def remove_fields_create(user_create: UserCreate, master_key: Optional[str] = Header(None)) -> UserCreate:
    if master_key != MASTER_KEY:
        user_create.is_superuser = False
        user_create.is_verified = False
    return user_create

async def superuser_authenticated_route(user: User = Depends(current_active_user)):
    # print(user)
    if not user.is_superuser:
        raise HTTPException(
            status_code=401, detail="You are not authorized to access this route"
        )