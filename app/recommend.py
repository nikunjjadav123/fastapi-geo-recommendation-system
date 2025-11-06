from sqlalchemy import func, select
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from app.models import POI
from app.config import settings

def geom_to_latlon(geom):
    if geom is None:
        return None, None
    point = to_shape(geom)
    return point.y, point.x  # latitude, longitude

def recommend(db: Session, lat: float, lon: float, radius_km: float = 10.0, limit: int = 20):
    radius_m = radius_km * 1000.0
    point = func.ST_SetSRID(func.ST_Point(lon, lat), 4326)
    distance_km = func.ST_DistanceSphere(POI.location, point) / 1000.0
    max_popularity = db.query(func.max(POI.popularity)).scalar() or 1
    score = (settings.alpha * (POI.popularity / max_popularity)) - (settings.beta * distance_km)

    query = (
        select(
            POI,
            distance_km.label("distance_km"),
            score.label("score")
        )
        .where(func.ST_DWithin(POI.location, point, radius_m))
        .order_by(score.desc())
        .limit(limit)
    )

    results = db.execute(query).all()  # returns list of Row tuples

    # Convert each POI and location to serializable dict
    serialized = []
    for poi, distance, score_val in results:
        lat, lon = geom_to_latlon(poi.location)
        serialized.append({
            "id": poi.id,
            "name": poi.name,
            "location": {"lat": lat, "lon": lon},
            "popularity": poi.popularity,
            "distance_km": distance,
            "score": score_val
        })

    return serialized
