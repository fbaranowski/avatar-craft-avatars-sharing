from motor.motor_asyncio import AsyncIOMotorClient

from settings import MongoSettings

MONGO_URI = f"mongodb://{MongoSettings.MONGO_USERNAME}:{MongoSettings.MONGO_PASSWORD}@mongodb:27017"

client = AsyncIOMotorClient(MONGO_URI)

db = client.get_database("shares")

shares_collection = db.get_collection("shares_collection")
