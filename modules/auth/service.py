from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import create_user, get_user_by_email
from .security import hash_password, verify_password, create_access_token
from .schemas import UserCreate, UserLogin


async def register_user(db: AsyncSession, data: UserCreate) -> dict:
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(data.password)
    user = await create_user(db, name=data.username, email=data.email, hashed_password=hashed)
    return {"message": "User registered successfully", "user_id": str(user.id)}


async def login_user(db: AsyncSession, data: UserLogin) -> dict:
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "name": user.name,
    }