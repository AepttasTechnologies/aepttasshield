import uuid
from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class VulnerabilityScan(Base):
    __tablename__ = "vulnerability_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String)
    file_size = Column(Integer)
    file_path = Column(String)
    scan_status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("vulnerability_scans.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    severity = Column(String)
    cwe_id = Column(String)
    location = Column(String)
    recommendation = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class VirusTotalScan(Base):
    __tablename__ = "virustotal_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_hash = Column(String)
    malicious = Column(Integer)
    suspicious = Column(Integer)
    harmless = Column(Integer)
    undetected = Column(Integer)
    verdict = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class YaraScan(Base):
    __tablename__ = "yara_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    scan_id = Column(UUID(as_uuid=True), ForeignKey("vulnerability_scans.id"))
    matched = Column(Boolean)
    total_matches = Column(Integer)
    matches = Column(JSONB)
    verdict = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class MlDetection(Base):
    __tablename__ = "ml_detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    scan_id = Column(UUID(as_uuid=True), ForeignKey("vulnerability_scans.id"))
    anomaly_score = Column(Float)
    is_anomaly = Column(Boolean)
    verdict = Column(String)
    features = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())


class GeoLocation(Base):
    __tablename__ = "geo_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())


class NearbyPlace(Base):
    __tablename__ = "nearby_places"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_name = Column(String)
    place_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    distance_km = Column(Float)

    
class VulnerabilityLog(Base):
    __tablename__ = "vulnerability_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String)
    method = Column(String)
    status = Column(Integer)
    ip = Column(String)
    response_time_ms = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class GeoAlert(Base):
    __tablename__ = "geo_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    severity = Column(String)
    ip = Column(String)
    alert_type = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class VulnerabilitySetting(Base):
    __tablename__ = "vulnerability_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    theme = Column(String)
    notifications_enabled = Column(Boolean)
    api_key = Column(String)
    updated_at = Column(TIMESTAMP, server_default=func.now())