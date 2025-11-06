from sqlalchemy import select, cast, Float,func
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from geoalchemy2 import Geography
from app.models import POI

def geom_to_latlon(geom):
    if geom is None:
        return None, None
    point = to_shape(geom)
    return point.y, point.x

def recommend(db: Session, lat: float, lon: float, radius_km: float = 10.0, limit: int = 10):
    radius_m = radius_km * 1000.0
    point = func.ST_SetSRID(func.ST_Point(lon, lat), 4326)

    distance_km = (func.ST_Distance(
        POI.location.cast(Geography(geometry_type='POINT', srid=4326)),
        func.ST_SetSRID(func.ST_Point(lon, lat), 4326).cast(Geography(geometry_type='POINT', srid=4326))
    ) / 1000.0).label("distance_km")

    query = select(POI, distance_km).where(
        func.ST_DWithin(
            POI.location.cast(Geography(geometry_type='POINT', srid=4326)),
            func.ST_SetSRID(func.ST_Point(lon, lat), 4326).cast(Geography(geometry_type='POINT', srid=4326)),
            radius_km * 1000.0
        )
    ).order_by(distance_km.asc()).limit(limit)

    results = db.execute(query).all()

    serialized = []
    for poi, distance in results:
        lat_val, lon_val = geom_to_latlon(poi.location)
        serialized.append({
            "id": poi.id,
            "name": poi.name,
            "location": {"lat": lat_val, "lon": lon_val},
            "popularity": poi.popularity,
            "distance_km": distance
        })

    return serialized
