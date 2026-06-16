from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_alerts_by_user


async def get_alerts(db: AsyncSession, user_id: int) -> list:
    alerts = await get_alerts_by_user(db, user_id)
    return [
        {
            "id": str(a.id),
            "severity": a.severity,
            "alert_type": a.alert_type,
            "ip": a.ip,
            "created_at": str(a.created_at),
        }
        for a in alerts
    ]