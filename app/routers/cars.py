from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from .. import crud, schemas
from ..database import get_db
from app.redis_client import redis_client
import json

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.get("/", response_model=List[schemas.Car])
async def read_cars(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    cache_key = f"cars:all:{skip}:{limit}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    cars = await crud.get_cars(db, skip=skip, limit=limit)
    await redis_client.set(
        cache_key,
        json.dumps([schemas.Car.model_validate(car).model_dump() for car in cars]),
        ex=60
    )
    return cars

@router.get("/by_brand/{brand}", response_model=List[schemas.Car])
async def get_cars_by_brand(brand: str, db: AsyncSession = Depends(get_db)):
    cache_key = f"cars:brand:{brand}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    cars = await crud.get_cars_by_brand(db, brand)
    await redis_client.set(cache_key, json.dumps([schemas.Car.model_validate(car).model_dump() for car in cars]), ex=60)
    return cars

@router.get("/by_engtype/{engtype}", response_model=List[schemas.Car])
async def get_cars_by_engtype(engtype: str, db: AsyncSession = Depends(get_db)):
    cache_key = f"cars:engtype:{engtype}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    cars = await crud.get_cars_by_engtype(db, engtype)
    await redis_client.set(cache_key, json.dumps([schemas.Car.model_validate(car).model_dump() for car in cars]), ex=60)
    return cars

@router.patch("/increase_price/{brand}", status_code=200)
async def increase_price_by_brand(
    brand: str,
    increment: float = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    await crud.increase_price_by_brand(db, brand, increment)
    # Invalidate relevant cache keys
    await redis_client.delete(f"cars:brand:{brand}")
    await redis_client.delete("cars:all:0:100")  # Optionally clear the main list cache
    return {"message": f"Prices for brand '{brand}' increased by {increment}."}
    