from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.auth.deps import get_current_user
from modules.geolocation import service

router = APIRouter(prefix="/api/v1/geolocation", tags=["Geolocation"])


class LocationInput(BaseModel):
    latitude: float
    longitude: float
    accuracy: float = 0.0


class NearbyInput(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 5.0


@router.get("/current")
async def get_current_location(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    location = await service.get_current_location(db=db, user_id=user_id)
    if not location:
        raise HTTPException(status_code=404, detail="No location found. Save a location first.")
    return location


@router.post("/save")
async def save_location(
    data: LocationInput,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    location = await service.save_location(db=db, user_id=user_id, latitude=data.latitude, longitude=data.longitude)
    return {"message": "Location saved successfully", "location": location}


@router.get("/history")
async def get_location_history(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    history = await service.get_location_history(db=db, user_id=user_id)
    return {"user_id": user_id, "total": len(history), "history": history}


@router.post("/nearby")
async def get_nearby_places(
    data: NearbyInput,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = int(current_user["sub"])
    places = await service.get_nearby_places(
        db=db, user_id=user_id,
        latitude=data.latitude, longitude=data.longitude,
        radius_km=data.radius_km,
    )
    return {"total": len(places), "radius_km": data.radius_km, "places": places}