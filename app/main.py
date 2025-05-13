from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers.notion_db_router import router as notion_db_router

load_dotenv()

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "alive"}

app.include_router(notion_db_router)