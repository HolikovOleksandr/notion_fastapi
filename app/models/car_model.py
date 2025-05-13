from pydantic import BaseModel
from typing import Optional

class Car(BaseModel):
    car_id: str
    name: str
    manufacturer: str
    year: int
    price: float
    color: Optional[str] = None