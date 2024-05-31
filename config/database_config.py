from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('MONGONAME')
password = os.getenv('PASSWORD')


uri = f"mongodb+srv://{username}:{password}@cluster0.cffsw2j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
db = client.Flight

users_collection = db["users"]
flights_collection = db["flights"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)