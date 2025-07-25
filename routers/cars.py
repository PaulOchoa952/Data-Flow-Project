from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.get("/", response_model=List[schemas.Car])
async def read_cars(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_cars(db, skip=skip, limit=limit)

@router.get("/{car_id}", response_model=schemas.Car)
async def read_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await crud.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=schemas.Car, status_code=201)
async def create_car(car: schemas.CarCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_car(db, car)

@router.put("/{car_id}", response_model=schemas.Car)
async def update_car(car_id: int, car: schemas.CarUpdate, db: AsyncSession = Depends(get_db)):
    db_car = await crud.update_car(db, car_id, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@router.delete("/{car_id}", response_model=schemas.Car)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    db_car = await crud.delete_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car
