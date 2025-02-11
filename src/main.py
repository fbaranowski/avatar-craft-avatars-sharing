from fastapi import FastAPI

from mongo_client import shares_collection
from routers import router as sharing_router

app = FastAPI()

app.include_router(sharing_router)


@app.on_event("startup")
async def startup():
    await shares_collection.create_index(
        [("from_user", 1), ("to_user", 1), ("avatar_id", 1)], unique=True
    )
