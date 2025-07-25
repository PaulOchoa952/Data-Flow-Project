from pydantic import BaseModel

class Car(BaseModel):
    brand: str
    price: float
    body: str
    mileage: int
    engv: float
    engtype: str
    registration: str
    year: int
    model: str
    drive: str

    model_config = {"from_attributes": True}