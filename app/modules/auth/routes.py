import logging

from bson import ObjectId
from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.exceptions import Conflict, DatabaseError, NotFound, Unauthorized
from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth.deps import get_current_user
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    db = get_db()
    if db is None:
        raise DatabaseError()

    try:
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
    except Conflict:
        raise
    except Exception as e:
        logger.error("Register error: %s", e)
        raise DatabaseError(str(e))


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    db = get_db()
    if db is None:
        raise DatabaseError()

    user = await db["users"].find_one({"username": body.username})
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise Unauthorized("Invalid credentials")

    token = create_access_token({"sub": str(user["_id"]), "username": user["username"]})
    return TokenResponse(access_token=token)


@router.get("/username-suggestions")
async def get_username_suggestions(q: str):
    db = get_db()
    if db is None:
        raise DatabaseError()
    cursor = db["users"].find(
        {"username": {"$regex": f"^{q}", "$options": "i"}},
        {"username": 1, "_id": 0},
    ).limit(10)
    return [doc["username"] async for doc in cursor]


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user = await db["users"].find_one({"_id": ObjectId(current_user["sub"])})
    if not user:
        raise NotFound("User not found")
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
