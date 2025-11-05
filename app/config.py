from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    host: str = "0.0.0.0"
    port: int = 8000
    items_per_page: int = 10
    alpha: float = 1.0
    beta: float = 0.1
    earth_radius: float = 6371.0  # Earth radius in kilometers

    class Config:
        env_file = ".env"

settings = Settings()