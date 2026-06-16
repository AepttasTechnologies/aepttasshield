from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import VulnerabilityScan, Vulnerability, VulnerabilityLog, GeoAlert


async def get_dashboard_stats(db: AsyncSession) -> dict:
    total_scans  = (await db.execute(select(func.count()).select_from(VulnerabilityScan))).scalar()
    total_vulns  = (await db.execute(select(func.count()).select_from(Vulnerability))).scalar()
    total_logs   = (await db.execute(select(func.count()).select_from(VulnerabilityLog))).scalar()
    total_alerts = (await db.execute(select(func.count()).select_from(GeoAlert))).scalar()

    high   = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "high"))).scalar()
    medium = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "medium"))).scalar()
    low    = (await db.execute(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "low"))).scalar()

    return {
        "total_scans": total_scans,
        "total_api_requests": total_logs,
        "total_vulnerabilities": total_vulns,
        "total_alerts": total_alerts,
        "vulnerability_breakdown": {"high": high, "medium": medium, "low": low},
    }


async def get_recent_activity(db: AsyncSession) -> list:
    logs   = (await db.execute(select(VulnerabilityLog).order_by(VulnerabilityLog.created_at.desc()).limit(10))).scalars().all()
    alerts = (await db.execute(select(GeoAlert).order_by(GeoAlert.created_at.desc()).limit(10))).scalars().all()

    activity = []
    for log in logs:
        activity.append({
            "time": str(log.created_at),
            "type": "log",
            "event": f"{log.method} {log.endpoint} → {log.status}",
            "ip": log.ip,
        })
    for alert in alerts:
        activity.append({
            "time": str(alert.created_at),
            "type": "alert",
            "event": alert.alert_type,
            "severity": alert.severity,
            "ip": alert.ip,
        })

    activity.sort(key=lambda x: x["time"], reverse=True)
    return activity[:20]