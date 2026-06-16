import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect(
        host='ep-nameless-queen-aqugbfe4-pooler.c-8.us-east-1.aws.neon.tech',
        port=5432,
        user='neondb_owner',
        password='npg_y9gXCVS3Klzd',
        database='neondb',
        ssl='require'
    )
    rows = await conn.fetch("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    for r in rows:
        print(r['table_name'])
    await conn.close()

asyncio.run(check())