from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.auth.deps import get_current_user
from modules.dashboard.service import get_dashboard_stats, get_recent_activity

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_dashboard_stats(db=db)


@router.get("/activity")
async def dashboard_activity(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_recent_activity(db=db)