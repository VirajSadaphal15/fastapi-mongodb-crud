
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection URL
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://localhost:27017/"
)

# Connect to MongoDB
client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

# Check database connection
client.admin.command("ping")

print("MongoDB Connected Successfully!")

# Create database
database = client["notes_database"]

# Create collection
notes_collection = database["notes"]
