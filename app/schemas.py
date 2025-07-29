from pydantic import BaseModel
from typing import Optional

class Car(BaseModel):
    id: Optional[int] = None
    brand: str
    price: float
    body: str
    mileage: int
    engv: Optional[float] = None
    engtype: str
    registration: str
    year: int
    model: str
    drive: str

    model_config = {"from_attributes": True}