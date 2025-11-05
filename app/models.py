from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String

from sqlalchemy import Column, DateTime, func
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class POI(Base):
    __tablename__ = "pois"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    popularity = Column(Integer, default=0)
    # store as WKT geometry POINT(lon lat) in PostGIS
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
