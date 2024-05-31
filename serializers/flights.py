from datetime import datetime

def serialize_flights(doc)->dict:
    return {
        "_id": str(doc["_id"]),
        "airline": str(doc["airline"]),
        "flightNumber": int(doc["flightNumber"]),
        "depCity": str(doc["depCity"]),
        "arrCity": str(doc["arrCity"]),
        "price": int(doc["price"]),
        "depDate": str(doc["depDate"]),
        "arrDate": str(doc["arrDate"]),
        "duration": str(doc["duration"]),
        "returnDate": doc["returnDate"].isoformat() if isinstance(doc["returnDate"], datetime) else str(doc["returnDate"]),
        "returnFlightNumber": str(doc["returnFlightNumber"]),
        "returnDepCity": str(doc["returnDepCity"]),
        "returnArrCity": str(doc["returnArrCity"]),
        "returnDuration": str(doc["returnDuration"]),
        "returnStops": int(doc["returnStops"])
    }



def decode_flights(docs) -> list:
    return [serialize_flights(doc) for doc in docs]