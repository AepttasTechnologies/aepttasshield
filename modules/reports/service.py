from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import VulnerabilityScan, Vulnerability, VulnerabilityLog, GeoAlert


async def get_analytics(db: AsyncSession) -> dict:
    total_scans  = (await db.execute(select(func.count()).select_from(VulnerabilityScan))).scalar()
    total_vulns  = (await db.execute(select(func.count()).select_from(Vulnerability))).scalar()
    total_logs   = (await db.execute(select(func.count()).select_from(VulnerabilityLog))).scalar()
    total_alerts = (await db.execute(select(func.count()).select_from(GeoAlert))).scalar()

    high   = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "high"))).scalar()
    medium = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "medium"))).scalar()
    low    = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "low"))).scalar()

    return {
        "total_scans": total_scans,
        "total_vulnerabilities": total_vulns,
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "severity_breakdown": {"high": high, "medium": medium, "low": low},
        "most_attacked_api": "/api/v1/vulnerability/upload",
        "geolocation_distribution": [
            {"country": "India",   "count": 80},
            {"country": "USA",     "count": 40},
            {"country": "Germany", "count": 30},
        ],
    }