from django import db
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import create_poi
from app.schemas import POICreate

SAMPLE = [
("Coffee Shop A", 12.9716, 77.5946, 80),
("Park B", 12.9750, 77.6000, 45),
("Museum C", 12.9800, 77.5900, 70),
]
def load_sample():
    db = SessionLocal()
    try:
        for name, lat, lon, pop in SAMPLE:
            create_poi(db, POICreate(name=name, lat=lat, lon=lon, popularity=pop))
    finally:
        db.close()


    if __name__ == '__main__':
        load_sample()