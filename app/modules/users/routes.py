from bson import ObjectId
from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.exceptions import BadRequest, Conflict, DatabaseError, NotFound
from app.core.security import hash_password
from app.modules.auth.deps import get_current_user
from app.modules.users.schemas import CreateUserRequest, UpdateUserRequest

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user.get("email", ""),
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", ""),
        "profile_pic": user.get("profile_pic", ""),
        "security_answer": user.get("security_answer", ""),
        "social_media": user.get("social_media", {}),
        "phone": user.get("phone", ""),
        "bio": user.get("bio", ""),
        "date_of_birth": user.get("date_of_birth", ""),
        "address": user.get("address", ""),
        "is_active": user.get("is_active", True),
        "role": user.get("role", "user"),
    }


@router.get("/")
async def list_users():
    db = get_db()
    if db is None:
        raise DatabaseError()
    users = await db["users"].find().to_list(100)
    return [serialize_user(u) for u in users]


@router.get("/{id}")
async def get_user(id: str):
    db = get_db()
    if db is None:
        raise DatabaseError()
    user = await db["users"].find_one({"_id": ObjectId(id)})
    if not user:
        raise NotFound("User not found")
    return serialize_user(user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(body: CreateUserRequest):
    db = get_db()
    if db is None:
        raise DatabaseError()
    existing = await db["users"].find_one({"$or": [{"username": body.username}, {"email": body.email}]})
    if existing:
        raise Conflict("Username or email already exists")
    user = {
        "username": body.username,
        "email": body.email,
        "hashed_password": hash_password(body.password),
        "first_name": body.first_name,
        "last_name": body.last_name,
        "profile_pic": body.profile_pic,
        "security_answer": body.security_answer,
        "social_media": body.social_media,
        "phone": body.phone,
        "bio": body.bio,
        "date_of_birth": body.date_of_birth,
        "address": body.address,
        "is_active": body.is_active,
        "role": body.role,
    }
    result = await db["users"].insert_one(user)
    return {"id": str(result.inserted_id), "username": body.username, "email": body.email, "first_name": body.first_name, "last_name": body.last_name, "role": body.role}


@router.put("/{id}")
async def update_user(id: str, body: UpdateUserRequest):
    db = get_db()
    if db is None:
        raise DatabaseError()
    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise BadRequest("No fields to update")
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    result = await db["users"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise NotFound("User not found")
    user = await db["users"].find_one({"_id": ObjectId(id)})
    return serialize_user(user)
