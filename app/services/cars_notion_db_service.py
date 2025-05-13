from typing import Optional, List
from notion_client import AsyncClient
from app.models.car_model import Car


class CarsNotionDbService:
    def __init__(self, notion_token: str, database_id: str):
        self.notion = AsyncClient(auth=notion_token)
        self.database_id = database_id

    async def create_new_car(self, car: Car) -> None:
        await self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Car ID": {"title": [{"text": {"content": str(car.car_id)}}]},
                "Name": {"rich_text": [{"text": {"content": car.name}}]},
                "Manufacturer": {"rich_text": [{"text": {"content": car.manufacturer}}]},
                "Year": {"number": car.year},
                "Price": {"number": car.price},
                "Color": {"rich_text": [{"text": {"content": car.color}}]} if car.color else {},
            }
        )

    async def read_all_cars(self) -> List[Car]:
        response = await self.notion.databases.query(self.database_id)
        cars: List[Car] = []

        for result in response.get("results", []):
            props = result.get("properties", {})

            car = Car(
                name=self._get_text(props, "Name") or "",
                manufacturer=self._get_text(props, "Manufacturer") or "",
                year=int(self._get_number(props, "Year") or 0),
                price=self._get_number(props, "Price") or 0.0,
                color=self._get_text(props, "Color") or None,
            )

            cars.append(car)
        return cars

    async def read_car_by_id(self, car_id: str) -> Optional[Car]:
        response = await self.notion.databases.query(
            self.database_id,
            filter={
                "property": "Car ID",
                "title": {"equals": car_id}
            }
        )

        if not response.get("results"):
            return None

        props = response["results"][0]["properties"]

        return Car(
            name=self._get_text(props, "Name") or "",
            manufacturer=self._get_text(props, "Manufacturer") or "",
            year=int(self._get_number(props, "Year") or 0),
            price=self._get_number(props, "Price") or 0.0,
            color=self._get_text(props, "Color") or None,
        )

    async def update_car_by_id(self, car_id: str, updates: dict) -> None:
        response = await self.notion.databases.query(
            self.database_id,
            filter={
                "property": "Car ID",
                "title": {"equals": car_id}
            }
        )

        if not response.get("results"):
            raise ValueError(f"Car with ID {car_id} not found")

        page_id = response["results"][0]["id"]
        properties = {}

        if "name" in updates:
            properties["Name"] = {"rich_text": [{"text": {"content": updates["name"]}}]}
        if "manufacturer" in updates:
            properties["Manufacturer"] = {"rich_text": [{"text": {"content": updates["manufacturer"]}}]}
        if "year" in updates:
            properties["Year"] = {"number": updates["year"]}
        if "price" in updates:
            properties["Price"] = {"number": updates["price"]}
        if "color" in updates:
            properties["Color"] = {"rich_text": [{"text": {"content": updates["color"]}}]}

        if properties:
            await self.notion.pages.update(
                page_id=page_id,
                properties=properties
            )

    async def delete_car_by_id(self, car_id: str) -> None:
        response = await self.notion.databases.query(
            self.database_id,
            filter={
                "property": "Car ID",
                "title": {"equals": car_id}
            }
        )

        if not response.get("results"):
            raise ValueError(f"Car with ID {car_id} not found")

        page_id = response["results"][0]["id"]
        await self.notion.pages.update(page_id=page_id, archived=True)

    def _get_text(self, props: dict, field: str, key: str = "rich_text") -> Optional[str]:
        try:
            return props[field][key][0]["text"]["content"]
        except (KeyError, IndexError, TypeError):
            return None

    def _get_number(self, props: dict, field: str) -> Optional[float]:
        return props.get(field, {}).get("number")
