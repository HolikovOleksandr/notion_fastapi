from typing import Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class Car(BaseModel):
    car_id: UUID = Field(default_factory=uuid4)
    name: str
    manufacturer: str
    year: int
    price: float
    color: Optional[str] = None