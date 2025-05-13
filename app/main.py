import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers.cars_router import CarsRouter
from app.services.cars_notion_db_service import CarsNotionDbService

load_dotenv()
app = FastAPI()


cars_router = CarsRouter(CarsNotionDbService(
    notion_token=os.getenv("NOTION_TOKEN", "your_notion_token"),
    database_id=os.getenv("NOTION_DB_ID", "your_notion_database_id"))
)

app.include_router(cars_router.router, prefix="/cars", tags=["Cars"])
