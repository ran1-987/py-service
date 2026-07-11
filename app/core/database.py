import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None


async def connect_db():
    global client
    try:
        client = AsyncIOMotorClient(settings.uri)
        await client.admin.command("ping")
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error("MongoDB connection failed: %s", e)
        client = None


async def close_db():
    global client
    if client:
        client.close()
        client = None


def get_db():
    return client.get_database("test") if client else None


def get_collection(name: str):
    db = get_db()
    return db[name] if db else None
