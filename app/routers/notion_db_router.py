from fastapi import APIRouter
from app.models.car_model import Car
from app.services.notion_db_service import add_car

router = APIRouter(prefix="/notion_db", tags=["Notion DB"])


@router.post("/cars")
def create_car(car: Car):
    add_car(car)
    return {"message": f"Car {car.name} added to Notion!"}