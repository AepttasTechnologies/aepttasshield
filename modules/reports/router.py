from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.auth.deps import get_current_user
from modules.reports import service

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.get("/analytics")
async def analytics(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_analytics(db=db)