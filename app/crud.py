from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Car
from .schemas import CarCreate, CarUpdate

async def get_car(db: AsyncSession, car_id: int):
    result = await db.execute(select(Car).where(Car.id == car_id))
    return result.scalar_one_or_none()

async def get_cars(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Car).offset(skip).limit(limit))
    return result.scalars().all()

async def create_car(db: AsyncSession, car: CarCreate):
    db_car = Car(**car.dict())
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)
    return db_car

async def update_car(db: AsyncSession, car_id: int, car: CarUpdate):
    db_car = await get_car(db, car_id)
    if db_car is None:
        return None
    for key, value in car.dict(exclude_unset=True).items():
        setattr(db_car, key, value)
    await db.commit()
    await db.refresh(db_car)
    return db_car

async def delete_car(db: AsyncSession, car_id: int):
    db_car = await get_car(db, car_id)
    if db_car is None:
        return None
    await db.delete(db_car)
    await db.commit()
    return db_car