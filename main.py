from contextlib import asynccontextmanager
from database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from modules.auth.router import router as auth_router
from modules.vulnerability.router import router as vulnerability_router
from modules.geolocation.router import router as geolocation_router
from modules.dashboard.router import router as dashboard_router
from modules.logs.router import router as logs_router
from modules.alerts.router import router as alerts_router
from modules.reports.router import router as reports_router
from modules.settings.router import router as settings_router

app = FastAPI(
    title="Mobile Application Security Suite",
    description="APK Vulnerability Scanner & Geolocation API",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True},
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": str(exc)})
# ── CORS ───────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTERS ────────────────────────────────────────────────────────────────
# FIX: each router already defines its own prefix — do NOT pass extra prefix= here.
# Old code was passing prefix="/api/v1/apk" on vulnerability_router which already
# had prefix="/api/v1/vulnerability", creating broken double-prefixed routes.
app.include_router(auth_router)           # /auth/register, /auth/login
app.include_router(vulnerability_router)  # /api/v1/vulnerability/...
app.include_router(geolocation_router)    # /api/v1/geolocation/...
app.include_router(dashboard_router)      # /api/v1/dashboard/...
app.include_router(logs_router)           # /api/v1/logs/...
app.include_router(alerts_router)         # /api/v1/alerts/...
app.include_router(reports_router)        # /api/v1/reports/...
app.include_router(settings_router)       # /api/v1/settings/...

# ── OPENAPI / SWAGGER AUTH ─────────────────────────────────────────────────
# FIX: was duplicated — add_security_scheme AND custom_openapi both assigned to
# app.openapi; last one won but had a bug (never stored schema).  One clean version:
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema.setdefault("components", {})["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply BearerAuth to every route so Swagger shows the lock icon
    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            if isinstance(operation, dict):
                operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi

# ── HEALTH CHECK ───────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Security Suite API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
