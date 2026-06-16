from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.auth.deps import get_current_user
from modules.settings.service import get_settings, update_settings

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])


@router.get("")
async def read_settings(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    return await get_settings(db=db, user_id=user_id)


@router.put("")
async def edit_settings(
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    return await update_settings(db=db, user_id=user_id, data=data)