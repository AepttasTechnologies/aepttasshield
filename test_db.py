import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "your_url_here"  # paste actual URL

async def test():
    engine = create_async_engine(DATABASE_URL, connect_args={"ssl": "require"})
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Connected!", result.fetchone())

asyncio.run(test())