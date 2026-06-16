from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.auth.deps import get_current_user
from modules.logs import service

router = APIRouter(prefix="/api/v1/logs", tags=["Logs"])


@router.get("")
async def get_logs(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    return await service.get_logs(db=db, user_id=user_id)