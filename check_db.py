"""
Quick diagnostic script - run with: python check_db.py
Checks row counts + sample row for the tables listed below.
Uses the same DATABASE_URL from your .env - no Neon console access needed.
"""

import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

TABLES_TO_CHECK = [
    "users",
    "vulnerability_scans",
    "vulnerabilities",
    "virustotal_scans",
    "yara_scans",
    "ml_detections",
    "geo_locations",
    "nearby_places",
    "vulnerability_logs",
    "geo_alerts",
    "vulnerability_settings",
]


async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.connect() as conn:
        for table in TABLES_TO_CHECK:
            print("=" * 60)
            print(f"TABLE: {table}")
            print("=" * 60)

            # Row count
            try:
                result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  Row count: {count}")
            except Exception as e:
                print(f"  ERROR counting rows: {e}")
                continue

            # Columns
            result = await conn.execute(
                text(
                    """
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = :table
                    ORDER BY ordinal_position
                    """
                ),
                {"table": table},
            )
            cols = result.fetchall()
            print("  Columns:")
            for c in cols:
                print(f"    {c[0]:<25} {c[1]:<20} nullable={c[2]:<5} default={c[3]}")

            # Sample row (if any)
            if count and count > 0:
                try:
                    result = await conn.execute(
                        text(f"SELECT * FROM {table} LIMIT 1")
                    )
                    row = result.mappings().fetchone()
                    print("  Sample row:")
                    for k, v in row.items():
                        print(f"    {k}: {v!r}")
                except Exception as e:
                    print(f"  ERROR fetching sample row: {e}")

            print()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())