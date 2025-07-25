from pydantic import BaseModel
from typing import Optional

class CarBase(BaseModel):
    brand: Optional[str]
    price: Optional[float]
    body: Optional[str]
    mileage: Optional[int]
    engv: Optional[float]
    engtype: Optional[str]
    registration: Optional[str]
    year: Optional[int]
    model: Optional[str]
    drive: Optional[str]

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class CarInDBBase(CarBase):
    id: int

    class Config:
        orm_mode = True

class Car(CarInDBBase):
    pass