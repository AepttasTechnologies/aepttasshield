from datetime import datetime
import uuid

# ── USERS ──────────────────────────────────────────────────────────────────
users_db: dict = {}

# ── APK SCANS ──────────────────────────────────────────────────────────────
apk_scans_db: dict = {}

# ── VULNERABILITIES ────────────────────────────────────────────────────────
vulnerabilities_db: dict = {}

# ── LOCATIONS ──────────────────────────────────────────────────────────────
locations_db: dict = {}

# ── NEARBY PLACES ──────────────────────────────────────────────────────────
nearby_places_db: dict = {}

# ── LOGS ───────────────────────────────────────────────────────────────────
logs_db: dict = {}

# ── ALERTS ─────────────────────────────────────────────────────────────────
alerts_db: dict = {}


# ── HELPERS ────────────────────────────────────────────────────────────────

def generate_id() -> str:
    return str(uuid.uuid4())

def get_timestamp() -> str:
    return datetime.utcnow().isoformat()


# ── USERS ──────────────────────────────────────────────────────────────────

def create_user(name: str, email: str, hashed_password: str) -> dict:
    user_id = generate_id()
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": get_timestamp(),
    }
    users_db[user_id] = user
    return user

def get_user_by_email(email: str) -> dict | None:
    for user in users_db.values():
        if user["email"] == email:
            return user
    return None

def get_user_by_id(user_id: str) -> dict | None:
    return users_db.get(user_id)


# ── APK SCANS ──────────────────────────────────────────────────────────────

def create_scan(user_id: str, file_name: str, file_size: int, file_path: str) -> dict:
    scan_id = generate_id()
    scan = {
        "id": scan_id,
        "user_id": user_id,
        "file_name": file_name,
        "file_size": file_size,
        "file_path": file_path,
        "scan_status": "pending",
        "created_at": get_timestamp(),
    }
    apk_scans_db[scan_id] = scan
    return scan

def get_scan_by_id(scan_id: str) -> dict | None:
    return apk_scans_db.get(scan_id)

def update_scan_status(scan_id: str, status: str) -> dict | None:
    scan = apk_scans_db.get(scan_id)
    if scan:
        scan["scan_status"] = status
    return scan

def get_all_scans() -> list:
    return list(apk_scans_db.values())


# ── VULNERABILITIES ────────────────────────────────────────────────────────

def create_vulnerability(scan_id: str, user_id: str, title: str,
                         description: str, severity: str, cwe_id: str,
                         location: str, recommendation: str) -> dict:
    vuln_id = generate_id()
    vuln = {
        "id": vuln_id,
        "scan_id": scan_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "severity": severity,
        "cwe_id": cwe_id,
        "location": location,
        "recommendation": recommendation,
        "created_at": get_timestamp(),
    }
    vulnerabilities_db[vuln_id] = vuln
    return vuln

def get_vulnerabilities_by_scan(scan_id: str) -> list:
    return [v for v in vulnerabilities_db.values() if v["scan_id"] == scan_id]

def get_all_vulnerabilities() -> list:
    return list(vulnerabilities_db.values())


# ── LOCATIONS ──────────────────────────────────────────────────────────────

def create_location(user_id: str, latitude: float,
                    longitude: float, accuracy: float) -> dict:
    location_id = generate_id()
    location = {
        "id": location_id,
        "user_id": user_id,
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": accuracy,
        "created_at": get_timestamp(),
    }
    locations_db[location_id] = location
    return location

def get_location_history(user_id: str) -> list:
    history = [l for l in locations_db.values() if l["user_id"] == user_id]
    return sorted(history, key=lambda x: x["created_at"], reverse=True)

def get_latest_location(user_id: str) -> dict | None:
    history = get_location_history(user_id)
    return history[0] if history else None


# ── NEARBY PLACES ──────────────────────────────────────────────────────────

def save_nearby_places(user_id: str, places: list) -> list:
    saved = []
    for place in places:
        place_id = generate_id()
        record = {
            "id": place_id,
            "user_id": user_id,
            "place_name": place.get("place_name"),
            "place_type": place.get("place_type"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
            "distance_km": place.get("distance_km"),
        }
        nearby_places_db[place_id] = record
        saved.append(record)
    return saved

def get_nearby_places(user_id: str) -> list:
    return [p for p in nearby_places_db.values() if p["user_id"] == user_id]


# ── LOGS ───────────────────────────────────────────────────────────────────

def create_log(user_id: str, endpoint: str, method: str,
               status: int, ip: str, response_time_ms: int) -> dict:
    log_id = generate_id()
    log = {
        "id": log_id,
        "user_id": user_id,
        "endpoint": endpoint,
        "method": method,
        "status": status,
        "ip": ip,
        "response_time_ms": response_time_ms,
        "created_at": get_timestamp(),
    }
    logs_db[log_id] = log
    return log

def get_logs_by_user(user_id: str) -> list:
    logs = [l for l in logs_db.values() if l["user_id"] == user_id]
    return sorted(logs, key=lambda x: x["created_at"], reverse=True)

def get_all_logs() -> list:
    return sorted(logs_db.values(), key=lambda x: x["created_at"], reverse=True)


# ── ALERTS ─────────────────────────────────────────────────────────────────

def create_alert(user_id: str, severity: str, ip: str, alert_type: str) -> dict:
    alert_id = generate_id()
    alert = {
        "id": alert_id,
        "user_id": user_id,
        "severity": severity,
        "ip": ip,
        "alert_type": alert_type,
        "created_at": get_timestamp(),
    }
    alerts_db[alert_id] = alert
    return alert

def get_alerts_by_user(user_id: str) -> list:
    alerts = [a for a in alerts_db.values() if a["user_id"] == user_id]
    return sorted(alerts, key=lambda x: x["created_at"], reverse=True)

def get_all_alerts() -> list:
    return sorted(alerts_db.values(), key=lambda x: x["created_at"], reverse=True)
