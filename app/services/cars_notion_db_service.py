from typing import Optional, List
from fastapi.concurrency import run_in_threadpool
from notion_client import AsyncClient
from app.models.car_model import Car



class CarsNotionDbService:
    def __init__(self, notion_token: str, database_id: str):
        self.notion = AsyncClient(auth=notion_token)
        self.database_id = database_id


    def create_new_car(self, car: Car):      
        self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Car ID": {"title": [{"text": {"content": car.car_id}}]},
                "Name": {"rich_text": [{"text": {"content": car.name}}]},
                "Manufacturer": {"rich_text": [{"text": {"content": car.manufacturer}}]},
                "Year": {"number": car.year},
                "Price": {"number": car.price},
                "Color": {"rich_text": [{"text": {"content": car.color}}]} if car.color else {},
            }
        )
        
        
    async def read_all_cars_from_db(self) -> List[Car]:
        response = await self.notion.databases.query(self.database_id)
        cars: List[Car] = []

        for result in response.get("results", []):
            props = result.get("properties", {})

            car = Car(
                car_id = self._get_text(props, "Car ID", "title") or "",
                name = self._get_text(props, "Name") or "",
                manufacturer = self._get_text(props, "Manufacturer") or "",
                year = int(self._get_number(props, "Year") or 0),
                price = self._get_number(props, "Price") or 0.0,
                color = self._get_text(props, "Color") or "",
            )

            cars.append(car)
        return cars


    def _get_text(self, props: dict, field: str, key: str = "rich_text") -> Optional[str]:
        try:
            return props[field][key][0]["text"]["content"]
        except (KeyError, IndexError, TypeError):
            return None
        

    def _get_number(self, props: dict, field: str) -> Optional[float]:
        return props.get(field, {}).get("number")
