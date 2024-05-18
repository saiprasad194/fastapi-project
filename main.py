from fastapi import FastAPI
from app.db.database import connect_to_db, create_tables
from app.db.base import *
from app.LDCS.routes import router
from app.users.routes import router as user_routes
import os
from app.config import get_config
import uvicorn

def get_application(config=os.getenv("ENV","dev")):
    settings = get_config(config=config)
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.include_router(user_routes, prefix="/api/v1")
    _app.include_router(router, prefix="/api/v1")
    return _app


app = get_application()


@app.on_event("startup")
async def startup_event():
    connect_to_db()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
