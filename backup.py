from config.database_config import flights_collection
import json
import os
import asyncio
from datetime import datetime


async def backup_flights():
    try:
        # Define backup directory path relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = os.path.join(script_dir, "backup")

        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Retrieve all documents from the flights collection
        flights_cursor = flights_collection.find()

        # Convert cursor to list of documents
        flights_list = await flights_cursor.to_list(length=None)

        # Convert ObjectId to string
        for flight in flights_list:
            flight["_id"] = str(flight["_id"])
            # Convert datetime objects to string representations
            for key, value in flight.items():
                if isinstance(value, datetime):
                    flight[key] = value.isoformat()

        # Define backup file path
        backup_file = os.path.join(backup_dir, "flights_backup.json")

        # Save the retrieved data to a JSON file in the backup directory
        with open(backup_file, "w") as file:
            json.dump(flights_list, file, indent=4)

        print(f"Backup successful! Data saved to {backup_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the backup function
async def main():
    await backup_flights()

# Run the main function in the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())