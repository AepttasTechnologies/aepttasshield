from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_logs_by_user


async def get_logs(db: AsyncSession, user_id: int) -> list:
    logs = await get_logs_by_user(db, user_id)
    return [
        {
            "id": str(l.id),
            "endpoint": l.endpoint,
            "method": l.method,
            "status": l.status,
            "ip": l.ip,
            "response_time_ms": l.response_time_ms,
            "created_at": str(l.created_at),
        }
        for l in logs
    ]