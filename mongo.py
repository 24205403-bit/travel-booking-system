
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["travel_booking"]

try:
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")
    print("Database:", db.name)

except Exception as e:
    print("MongoDB connection failed:", e)
