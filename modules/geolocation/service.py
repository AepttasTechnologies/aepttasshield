import math
from sqlalchemy.ext.asyncio import AsyncSession
from crud import create_geo_location, get_geo_locations_by_user, create_nearby_place, get_nearby_places_by_user

MOCK_NEARBY_PLACES = [
    {"place_name": "Police Station, Connaught Place", "place_type": "police",   "lat_offset": 0.012, "lng_offset": 0.008},
    {"place_name": "Hospital, RML",                   "place_type": "hospital", "lat_offset": 0.018, "lng_offset": 0.015},
    {"place_name": "Fire Station, Civil Lines",        "place_type": "fire",     "lat_offset": 0.022, "lng_offset": 0.020},
    {"place_name": "ATM, SBI Branch",                  "place_type": "atm",      "lat_offset": 0.006, "lng_offset": 0.004},
]


def _haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lng / 2) ** 2)
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


async def save_location(db: AsyncSession, user_id: int, latitude: float, longitude: float, accuracy: float = 0.0) -> dict:
    loc = await create_geo_location(db=db, user_id=user_id, latitude=latitude, longitude=longitude, accuracy=accuracy)
    return {"id": str(loc.id), "latitude": loc.latitude, "longitude": loc.longitude}


async def get_current_location(db: AsyncSession, user_id: int) -> dict | None:
    history = await get_geo_locations_by_user(db, user_id)
    if not history:
        return None
    loc = history[-1]
    return {"id": str(loc.id), "latitude": loc.latitude, "longitude": loc.longitude, "created_at": str(loc.created_at)}


async def get_location_history(db: AsyncSession, user_id: int) -> list:
    history = await get_geo_locations_by_user(db, user_id)
    return [
        {"id": str(l.id), "latitude": l.latitude, "longitude": l.longitude, "created_at": str(l.created_at)}
        for l in history
    ]


async def get_nearby_places(db: AsyncSession, user_id: int, latitude: float, longitude: float, radius_km: float) -> list:
    places = []
    for place in MOCK_NEARBY_PLACES:
        place_lat = latitude + place["lat_offset"]
        place_lng = longitude + place["lng_offset"]
        distance = _haversine_km(latitude, longitude, place_lat, place_lng)
        if distance <= radius_km:
            await create_nearby_place(
                db=db,
                user_id=user_id,
                place_name=place["place_name"],
                place_type=place["place_type"],
                latitude=round(place_lat, 4),
                longitude=round(place_lng, 4),
                distance_km=distance,
            )
            places.append({
                "place_name": place["place_name"],
                "place_type": place["place_type"],
                "latitude": round(place_lat, 4),
                "longitude": round(place_lng, 4),
                "distance_km": distance,
            })
    return sorted(places, key=lambda x: x["distance_km"])