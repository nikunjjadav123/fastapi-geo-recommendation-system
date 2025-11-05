from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models import POI  # Make sure POI has `geom` as Geometry
from app.schemas import POICreate
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

def create_poi(db: Session, poi: POICreate):
    """
    Create a new POI in the database with a geometry point.
    """
    # Create geometry point with SRID 4326
    geom = from_shape(Point(poi.lon, poi.lat), srid=4326)

    existing_poi = db.query(POI).filter(
        POI.location.ST_Equals(geom)
    ).first()
    if existing_poi:
        # Duplicate found, raise an error
        raise HTTPException(status_code=400, detail="POI with these coordinates already exists")
    # Set default popularity if not provided
    popularity = poi.popularity if poi.popularity is not None else 0

    db_poi = POI(
        name=poi.name,
        description=poi.description,
        popularity=popularity,
        location=geom
    )

    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi


def list_pois(db: Session, limit: int = 100):
    """
    List POIs with an optional limit.
    """
    return db.query(POI).limit(limit).all()
