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
        SELECT table_name, column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name IN (
            'vulnerability_scans','vulnerabilities','virustotal_scans',
            'yara_scans','ml_detections','geo_locations','nearby_places',
            'vulnerability_logs','geo_alerts','vulnerability_settings','users'
        )
        ORDER BY table_name, ordinal_position
    """)
    for r in rows:
        print(f"{r['table_name']:30} {r['column_name']:25} {r['data_type']}")
    await conn.close()

asyncio.run(check())