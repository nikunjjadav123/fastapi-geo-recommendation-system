from pydantic import BaseModel, Field
from typing import Optional

class POICreate(BaseModel):
    name: str = Field(..., description="Name of the point of interest")
    description: Optional[str] = Field(None, description="Optional description")
    popularity: int = Field(0, description="Popularity score, default is 0")
    lat: float = Field(..., description="Latitude of the POI")
    lon: float = Field(..., description="Longitude of the POI")


class POIRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    popularity: int
    lat: float
    lon: float
