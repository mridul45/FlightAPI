from fastapi import APIRouter,Query,HTTPException
from models.flights import Flight
from config.database_config import flights_collection
from serializers.flights import serialize_flights, decode_flights
import datetime
import bcrypt
from bson import ObjectId
from typing import List, Optional

router = APIRouter(
    prefix='/flights',
    tags=['Flights']
)


@router.get("", response_model=list[Flight])
async def get_flights():

    flights_cursor = flights_collection.find()
    flights_list = await flights_cursor.to_list(length=None)  # Convert cursor to list
    data = decode_flights(flights_list)
    return data


@router.post("")
async def create_flight(doc: Flight):

    doc = doc.dict()

    current_date = datetime.date.today()
    doc["date"] = str(current_date)

    res = await flights_collection.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status": "Ok",
        "message": "User Created",
        "_id": doc_id
    }


@router.get("price_range",response_model=List[Flight])
async def get_flights_by_price_range(
    min_price: Optional[int] = Query(None,alias="minPrice"),
    max_price: Optional[int] = Query(None,alias="maxPrice")
):
    
    query = {}
    if min_price is not None and max_price is not None:
        query["price"] = {"$gt": min_price, "$lte": max_price}

    elif min_price is not None:
        query["price"] = {"$gte": min_price}

    elif max_price is not None:
        query["price"] = {"$lte": max_price}

    
    flights_cursor = flights_collection.find(query)
    flights_list = await flights_cursor.to_list(length=None)
    data = decode_flights(flights_list)
    return data


@router.get("one-way", response_model=List[Flight])
async def search_one_way_flights(
    dep_city: str,
    arr_city: str,
    dep_date: str
):
    # Validate dep_date
    try:
        dep_date = datetime.datetime.strptime(dep_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    query = {
        "depCity": dep_city,
        "arrCity": arr_city,
        "depDate": {"$gte": dep_date.isoformat()}
    }

    flights_cursor = flights_collection.find(query)
    flights_list = await flights_cursor.to_list(length=None)
    data = decode_flights(flights_list)
    return data



@router.get("return", response_model=List[Flight])
async def search_return_flights(
    dep_city: str,
    arr_city: str,
    dep_date: str,
    return_date: str
):
    # Validate dep_date and return_date
    try:
        dep_date = datetime.datetime.strptime(dep_date, "%Y-%m-%d")
        return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    query = {
        "depCity": dep_city,
        "arrCity": arr_city,
        "depDate": {"$gte": dep_date.isoformat()},
        "returnDate": {"$gte": return_date.isoformat()}
    }

    flights_cursor = flights_collection.find(query)
    flights_list = await flights_cursor.to_list(length=None)
    data = decode_flights(flights_list)
    return data