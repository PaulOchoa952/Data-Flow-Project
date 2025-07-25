from fastapi import FastAPI
from .routers import cars

app = FastAPI(
    title="Car API",
    description="API for managing cars",
    version="1.0.0"
)

app.include_router(cars.router)