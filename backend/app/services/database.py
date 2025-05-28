from pymongo import MongoClient
from dotenv import load_dotenv
import os
import asyncio
from functools import wraps

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb_image_moderation:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "image_moderation")

# Global client and db reference
_client = None
_db = None

def run_in_executor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper

def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client

def get_database():
    global _db
    if _db is None:
        client = get_mongo_client()
        _db = client[DATABASE_NAME]
    return _db

# Collection dependency functions
async def get_tokens_collection():
    db = get_database()
    return db.tokens

async def get_usages_collection():
    db = get_database()
    return db.usages

# Startup function to initialize connection
async def connect_to_mongo():
    global _client, _db
    _client = MongoClient(MONGO_URI)
    _db = _client[DATABASE_NAME]
    # Test the connection
    try:
        _db.command('ping')
        print("Connected to MongoDB successfully")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

# Cleanup function
async def close_mongo_connection():
    global _client
    if _client:
        _client.close()
        _client = None