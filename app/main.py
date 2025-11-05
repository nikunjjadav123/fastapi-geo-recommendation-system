from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from app.database import SessionLocal, init_db,Base
from app import crud, schemas,recommend

app = FastAPI(title="Geo Recommendation API")

@app.on_event("startup")
def on_startup():
    # Initialize database tables
    init_db()
    print("Tables in metadata:", Base.metadata.tables.keys())


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper function to convert Geometry column to lat/lon
def geom_to_latlon(geom):
    if geom is None:
        return None, None
    point = to_shape(geom)
    return point.y, point.x  # latitude, longitude


@app.post("/pois", response_model=schemas.POIRead)
def create_poi(poi: schemas.POICreate, db: Session = Depends(get_db)):
    # Create POI using CRUD
    created = crud.create_poi(db, poi)
    if not created:
        raise HTTPException(status_code=400, detail="Could not create POI")

    # Convert geom to lat/lon using the correct column
    lat, lon = geom_to_latlon(created.location)

    # Return response matching POIRead schema
    return {
        "id": created.id,
        "name": created.name,
        "description": created.description,
        "popularity": getattr(created, "popularity", 0),
        "lat": lat,
        "lon": lon,
    }


@app.get("/recommend")
def get_recommend(
    lat: float,
    lon: float,
    radius_km: float = 10.0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    results = recommend.recommend(db, lat=lat, lon=lon, radius_km=radius_km, limit=limit)

    return {"count": len(results), "results": results}
