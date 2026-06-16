from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_settings_by_user, upsert_vulnerability_setting


async def get_settings(db: AsyncSession, user_id: int) -> dict:
    setting = await get_settings_by_user(db, user_id)
    if not setting:
        return {}
    return {
        "theme": setting.theme,
        "notifications_enabled": setting.notifications_enabled,
        "api_key": setting.api_key,
    }


async def update_settings(db: AsyncSession, user_id: int, data: dict) -> dict:
    setting = await upsert_vulnerability_setting(
        db=db,
        user_id=user_id,
        theme=data.get("theme"),
        notifications_enabled=data.get("notifications_enabled"),
        api_key=data.get("api_key"),
    )
    return {
        "theme": setting.theme,
        "notifications_enabled": setting.notifications_enabled,
        "api_key": setting.api_key,
    }