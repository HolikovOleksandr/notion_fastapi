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
        self.router.add_api_route("/{car_id}", self.read_car_by_id, methods=["GET"])
        self.router.add_api_route("/{car_id}", self.update_car_by_id, methods=["PATCH"])
        self.router.add_api_route("/{car_id}", self.delete_car_by_id, methods=["DELETE"])
        
        
    async def create_new_car(self, car: Car):
        await self.notion_service.create_new_car(car)  
        return {"message": f"Car with ID {car.car_id}  created successfully"}  
    
    
    async def read_car_by_id(self, car_id: str) -> Car:
        car = await self.notion_service.read_car_by_id(car_id)
        if car is None: raise ValueError(f"Car with ID {car_id} not found")
        return car
    
    
    async def update_car_by_id(self, car_id: str, updates: dict):
        await self.notion_service.update_car_by_id(car_id, updates)
        return {"message": f"Car with ID {car_id} updated successfully"}


    async def delete_car_by_id(self, car_id: str):
        await self.notion_service.delete_car_by_id(car_id)
        return {"message": f"Car with ID {car_id} deleted successfully"}
    

    async def get_all_cars(self) -> List[Car]:
        return await self.notion_service.read_all_cars()
