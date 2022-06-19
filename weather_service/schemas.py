from pydantic import BaseModel


class Coord(BaseModel):
    lon: float
    lat: float


class WeatherSchema(BaseModel):
    city: str
    temp: float
    temp_min: float
    temp_max: float
    coord: Coord
