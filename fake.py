import random
from datetime import datetime, timedelta
from faker import Faker
from config.database_config import client,flights_collection
import asyncio


fake = Faker()

def generate_flight():
    dep_date = fake.date_time_between(start_date='now', end_date='+30d')
    arr_date = dep_date + timedelta(hours=random.randint(1, 12))
    return_date = arr_date + timedelta(days=random.randint(1, 15))
    return {
        "airline": fake.company(),
        "flightNumber": random.randint(1000, 9999),
        "depCity": fake.city(),
        "arrCity": fake.city(),
        "price": random.randint(100, 1000),
        "depDate": dep_date.isoformat(),
        "arrDate": arr_date.isoformat(),
        "duration": str((arr_date - dep_date).seconds // 3600) + " Hours",
        "returnDate": return_date.isoformat(),
        "returnFlightNumber": str(random.randint(1000, 9999)),
        "returnDepCity": fake.city(),
        "returnArrCity": fake.city(),
        "returnDuration": str(random.randint(1, 12)) + " hours",
        "returnStops": random.randint(0, 3),
        "date": dep_date.date().isoformat()
    }

# Asynchronous function to insert multiple documents
async def insert_flights():
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        # Generate and insert multiple documents
        documents = [generate_flight() for _ in range(200)]
        await flights_collection.insert_many(documents)
        print("Inserted 200 flight documents into the collection.")
    except Exception as e:
        print(e)

# Get the current event loop and run the insertion
loop = asyncio.get_event_loop()
loop.run_until_complete(insert_flights())