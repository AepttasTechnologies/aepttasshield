from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    User, VulnerabilityScan, Vulnerability, VirusTotalScan,
    YaraScan, MlDetection, GeoLocation, NearbyPlace,
    VulnerabilityLog, GeoAlert, VulnerabilitySetting
)

# ── USERS ────────────────────────────────────────────────────────────────

async def create_user(db: AsyncSession, name: str, email: str, hashed_password: str) -> User:
    user = User(name=name, email=email, password_hash=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ── VULNERABILITY SCANS ──────────────────────────────────────────────────

async def create_vulnerability_scan(db: AsyncSession, user_id: int, file_name: str, file_size: int = 0, file_path: str = "") -> VulnerabilityScan:
    scan = VulnerabilityScan(user_id=user_id, file_name=file_name, file_size=file_size, file_path=file_path, scan_status="pending")
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    return scan

async def get_vulnerability_scan(db: AsyncSession, scan_id) -> VulnerabilityScan | None:
    result = await db.execute(select(VulnerabilityScan).where(VulnerabilityScan.id == scan_id))
    return result.scalar_one_or_none()

async def update_scan_status(db: AsyncSession, scan_id, status: str):
    scan = await get_vulnerability_scan(db, scan_id)
    if scan:
        scan.scan_status = status
        await db.commit()
        await db.refresh(scan)
    return scan

async def get_scans_by_user(db: AsyncSession, user_id: int) -> list[VulnerabilityScan]:
    result = await db.execute(select(VulnerabilityScan).where(VulnerabilityScan.user_id == user_id))
    return result.scalars().all()

# ── VULNERABILITIES ──────────────────────────────────────────────────────

async def create_vulnerability(db: AsyncSession, scan_id, user_id: int, title: str, description: str, severity: str, cwe_id: str, location: str, recommendation: str) -> Vulnerability:
    vuln = Vulnerability(scan_id=scan_id, user_id=user_id, title=title, description=description, severity=severity, cwe_id=cwe_id, location=location, recommendation=recommendation)
    db.add(vuln)
    await db.commit()
    await db.refresh(vuln)
    return vuln

async def get_vulnerabilities_by_scan(db: AsyncSession, scan_id) -> list[Vulnerability]:
    result = await db.execute(select(Vulnerability).where(Vulnerability.scan_id == scan_id))
    return result.scalars().all()

# ── VIRUSTOTAL SCANS ─────────────────────────────────────────────────────

async def create_virustotal_scan(db: AsyncSession, user_id: int, file_hash: str, malicious: int, suspicious: int, harmless: int, undetected: int, verdict: str) -> VirusTotalScan:
    vt = VirusTotalScan(user_id=user_id, file_hash=file_hash, malicious=malicious, suspicious=suspicious, harmless=harmless, undetected=undetected, verdict=verdict)
    db.add(vt)
    await db.commit()
    await db.refresh(vt)
    return vt

async def get_virustotal_by_user(db: AsyncSession, user_id: int) -> list[VirusTotalScan]:
    result = await db.execute(select(VirusTotalScan).where(VirusTotalScan.user_id == user_id))
    return result.scalars().all()

# ── YARA SCANS ───────────────────────────────────────────────────────────

async def create_yara_scan(db: AsyncSession, user_id: int, scan_id, matched: bool, total_matches: int, matches: dict, verdict: str) -> YaraScan:
    yara = YaraScan(user_id=user_id, scan_id=scan_id, matched=matched, total_matches=total_matches, matches=matches, verdict=verdict)
    db.add(yara)
    await db.commit()
    await db.refresh(yara)
    return yara

async def get_yara_scan(db: AsyncSession, scan_id) -> YaraScan | None:
    result = await db.execute(select(YaraScan).where(YaraScan.scan_id == scan_id))
    return result.scalar_one_or_none()

# ── ML DETECTIONS ────────────────────────────────────────────────────────

async def create_ml_detection(db: AsyncSession, user_id: int, scan_id, anomaly_score: float, is_anomaly: bool, verdict: str, features: dict) -> MlDetection:
    ml = MlDetection(user_id=user_id, scan_id=scan_id, anomaly_score=anomaly_score, is_anomaly=is_anomaly, verdict=verdict, features=features)
    db.add(ml)
    await db.commit()
    await db.refresh(ml)
    return ml

async def get_ml_detection(db: AsyncSession, scan_id) -> MlDetection | None:
    result = await db.execute(select(MlDetection).where(MlDetection.scan_id == scan_id))
    return result.scalar_one_or_none()

# ── GEO LOCATIONS ────────────────────────────────────────────────────────

async def create_geo_location(db: AsyncSession, user_id: int, latitude: float, longitude: float, accuracy: float = 0.0) -> GeoLocation:
    loc = GeoLocation(user_id=user_id, latitude=latitude, longitude=longitude, accuracy=accuracy)
    db.add(loc)
    await db.commit()
    await db.refresh(loc)
    return loc

async def get_geo_locations_by_user(db: AsyncSession, user_id: int) -> list[GeoLocation]:
    result = await db.execute(select(GeoLocation).where(GeoLocation.user_id == user_id))
    return result.scalars().all()

# ── NEARBY PLACES ────────────────────────────────────────────────────────

async def create_nearby_place(db: AsyncSession, user_id: int, place_name: str, place_type: str, latitude: float, longitude: float, distance_km: float) -> NearbyPlace:
    place = NearbyPlace(user_id=user_id, place_name=place_name, place_type=place_type, latitude=latitude, longitude=longitude, distance_km=distance_km)
    db.add(place)
    await db.commit()
    await db.refresh(place)
    return place

async def get_nearby_places_by_user(db: AsyncSession, user_id: int) -> list[NearbyPlace]:
    result = await db.execute(select(NearbyPlace).where(NearbyPlace.user_id == user_id))
    return result.scalars().all()

# ── VULNERABILITY LOGS ───────────────────────────────────────────────────

async def create_vulnerability_log(db: AsyncSession, user_id: int, endpoint: str, method: str, status: int, ip: str = "internal", response_time_ms: int = 0) -> VulnerabilityLog:
    log = VulnerabilityLog(user_id=user_id, endpoint=endpoint, method=method, status=status, ip=ip, response_time_ms=response_time_ms)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def get_logs_by_user(db: AsyncSession, user_id: int) -> list[VulnerabilityLog]:
    result = await db.execute(select(VulnerabilityLog).where(VulnerabilityLog.user_id == user_id))
    return result.scalars().all()

# ── GEO ALERTS ───────────────────────────────────────────────────────────

async def create_geo_alert(db: AsyncSession, user_id: int, severity: str, alert_type: str, ip: str = "internal") -> GeoAlert:
    alert = GeoAlert(user_id=user_id, severity=severity, alert_type=alert_type, ip=ip)
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert

async def get_alerts_by_user(db: AsyncSession, user_id: int) -> list[GeoAlert]:
    result = await db.execute(select(GeoAlert).where(GeoAlert.user_id == user_id))
    return result.scalars().all()

# ── VULNERABILITY SETTINGS ───────────────────────────────────────────────

async def get_settings_by_user(db: AsyncSession, user_id: int) -> VulnerabilitySetting | None:
    result = await db.execute(select(VulnerabilitySetting).where(VulnerabilitySetting.user_id == user_id))
    return result.scalar_one_or_none()

async def upsert_vulnerability_setting(db: AsyncSession, user_id: int, theme: str = None, notifications_enabled: bool = None, api_key: str = None) -> VulnerabilitySetting:
    setting = await get_settings_by_user(db, user_id)
    if not setting:
        setting = VulnerabilitySetting(user_id=user_id)
        db.add(setting)
    if theme is not None:
        setting.theme = theme
    if notifications_enabled is not None:
        setting.notifications_enabled = notifications_enabled
    if api_key is not None:
        setting.api_key = api_key
    await db.commit()
    await db.refresh(setting)
    return setting