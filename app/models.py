from sqlalchemy import Column, Integer, String, Double
from .database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand = Column(String(255))
    price = Column(Double)
    body = Column(String(255))
    mileage = Column(Integer)
    engv = Column(Double)
    engtype = Column(String(255))
    registration = Column(String(10))
    year = Column(Integer)
    model = Column(String(255))
    drive = Column(String(255))    