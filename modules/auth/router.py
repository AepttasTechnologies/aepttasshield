from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from .service import login_user, register_user
from .schemas import UserLogin, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    return await register_user(db, data)


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login and receive a JWT bearer token."""
    return await login_user(db, data)