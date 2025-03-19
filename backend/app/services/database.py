import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB Atlas
client = AsyncIOMotorClient(MONGO_URI)
db = client["linkedin_post_bot"]  # Database name

# Define collections
users_collection = db["users"]
posts_collection = db["posts"]
