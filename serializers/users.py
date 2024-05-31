def serialize_users(doc)->dict:
    return {
        "_id": str(doc["_id"]),
        "name": str(doc["name"]),
        "email": str(doc["email"]),
        "age": int(doc["age"])
    }

def decode_users(docs) -> list:
    return [serialize_users(doc) for doc in docs]