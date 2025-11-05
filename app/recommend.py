from sqlalchemy.orm import Session
from math import radians, cos, sin, asin, sqrt
from geoalchemy2.shape import to_shape
from app.models import POI
from app.config import settings

# Haversine formula to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = settings.earth_radius  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# Helper to convert geometry to lat/lon
def geom_to_latlon(geom):
    if geom is None:
        return None, None
    point = to_shape(geom)
    return point.y, point.x  # latitude, longitude

def recommend(db: Session, lat: float, lon: float, radius_km: float = 10.0, limit: int = 20):
    # Fetch all POIs from database
    pois = db.query(POI).all()

    # Prevent division by zero
    max_popularity = max((p.popularity for p in pois), default=1)
    
    results = []

    for p in pois:
        poi_lat, poi_lon = geom_to_latlon(p.location)  # extract lat/lon from geometry
        if poi_lat is None or poi_lon is None:
            continue

        distance_km = haversine(lat, lon, poi_lat, poi_lon)
        if distance_km <= radius_km:
            score = (settings.alpha * (p.popularity / max_popularity)) - (settings.beta * distance_km)
            results.append({
                "id": p.id,
                "name": p.name,
                "popularity": p.popularity,
                "distance_km": distance_km,
                "score": score,
                "lat": poi_lat,
                "lon": poi_lon
            })

    # Sort by score descending and return top N
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]
