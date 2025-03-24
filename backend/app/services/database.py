import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load .env for local dev (ignored in CI/CD)
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI is not set in environment variables.")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()  # Use DB from URI

# Define collections
users_collection = db["users"]
posts_collection = db["posts"]
