from fastapi import APIRouter
from app.services.cars_notion_db_service import CarsNotionDbService
from app.models.car_model import Car
from typing import List

class CarsRouter:
    def __init__(self, notion_service: CarsNotionDbService):
        self.router = APIRouter()
        self.notion_service = notion_service
        self._setup_routes()
        

    def _setup_routes(self):
        self.router.add_api_route("/", self.create_new_car, methods=["POST"])
        self.router.add_api_route("/", self.get_all_cars, methods=["GET"])
        
        
    def create_new_car(self, car: Car):
        self.notion_service.create_new_car(car)  
        return {"message": f"Car {car.name} created successfully"}  
        

    async def get_all_cars(self) -> List[Car]:
        return await self.notion_service.read_all_cars_from_db()
