from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Car
from sqlalchemy import update
from fastapi import Body
from fastapi import Depends
from app.database import get_db
from fastapi import APIRouter

router = APIRouter()

async def get_cars(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Car).offset(skip).limit(limit))
    return result.scalars().all()

async def get_cars_by_brand(db: AsyncSession, brand: str, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Car).where(Car.brand == brand).offset(skip).limit(limit))
    return result.scalars().all()

async def get_cars_by_engtype(db: AsyncSession, engtype: str, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Car).where(Car.engtype == engtype).offset(skip).limit(limit))
    return result.scalars().all()

async def increase_price_by_brand(db: AsyncSession, brand: str, increment: float):
    stmt = (
        update(Car)
        .where(Car.brand == brand)
        .values(price=Car.price + increment)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
