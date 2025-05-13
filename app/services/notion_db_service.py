import os
from notion_client import Client
from app.models.car_model import Car


notion = Client(auth=os.environ["NOTION_TOKEN"])
NOTION_DB_ID = os.environ["NOTION_DB_ID"]


def add_car(car: Car):
    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "Car ID": {"title": [{"text": {"content": car.car_id}}]},
            "Name": {"rich_text": [{"text": {"content": car.name}}]},
            "Manufacturer": {"rich_text": [{"text": {"content": car.manufacturer}}]},
            "Year": {"number": car.year},
            "Price": {"number": car.price},
            "Color": {"rich_text": [{"text": {"content": car.color}}]},
        }
    )