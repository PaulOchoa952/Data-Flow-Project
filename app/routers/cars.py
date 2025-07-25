from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.get("/", response_model=List[schemas.Car])
async def read_cars(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_cars(db, skip=skip, limit=limit)

@router.get("/by_brand/{brand}", response_model=List[schemas.Car])
async def get_cars_by_brand(brand: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_cars_by_brand(db, brand)

@router.get("/by_engtype/{engtype}", response_model=List[schemas.Car])
async def get_cars_by_engtype(engtype: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_cars_by_engtype(db, engtype)

@router.patch("/increase_price/{brand}", status_code=200)
async def increase_price_by_brand(
    brand: str,
    increment: float = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    await crud.increase_price_by_brand(db, brand, increment)
    return {"message": f"Prices for brand '{brand}' increased by {increment}."}
    