from fastapi import APIRouter 
from models.users import UserRegister , UserDetail,UpdateUser
from config.database_config import users_collection
from serializers.users import serialize_users, decode_users
import datetime
import bcrypt
from bson import ObjectId

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get("", response_model=list[UserDetail])
async def get_users():

    users_cursor = users_collection.find()
    users_list = await users_cursor.to_list(length=None)  # Convert cursor to list
    data = decode_users(users_list)
    return data

@router.post("")
async def create_user(doc: UserRegister):

    doc = doc.dict()

    hashed_password = bcrypt.hashpw(doc['password'].encode('utf-8'), bcrypt.gensalt())
    doc['password'] = hashed_password.decode('utf-8')

    current_date = datetime.date.today()
    doc["date"] = str(current_date)

    res = await users_collection.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status": "Ok",
        "message": "User Created",
        "_id": doc_id
    }


@router.get("/{_id}")
async def get_user(_id: str):
    user_doc = await users_collection.find_one({"_id": ObjectId(_id)})
    if user_doc:
        user_detail = UserDetail(**user_doc)
        return user_detail
    else:
        return {"message": "User not found"}
    


@router.put("/{_id}")
async def update_user(_id: str,doc: UpdateUser):
    req = dict(doc.model_dump(exclude_unset=True))
    await users_collection.find_one_and_update(
        {"_id": ObjectId(_id)},
        {"$set": req}
    )

    return {
        "status": "OK",
        "message": "Blog Updated successfully"
    }



@router.delete("/{_id}")
async def delete_user(_id: str):

    await users_collection.find_one_and_delete(
        {"_id": ObjectId(_id)}
    )
    return {
        "status": "OK",
        "message": "Blog Deleted successfully"
    }