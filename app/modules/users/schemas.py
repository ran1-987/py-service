import re
from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    profile_pic: str = ""
    security_answer: str = ""
    social_media: dict = {}
    phone: str = ""
    bio: str = ""
    date_of_birth: str = ""
    address: str = ""
    is_active: bool = True
    role: Literal["user", "admin"] = "user"

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must be alphanumeric (letters, numbers, underscores)")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v and len(v) < 1:
            raise ValueError("Name cannot be empty if provided")
        return v


class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    profile_pic: str | None = None
    security_answer: str | None = None
    social_media: dict | None = None
    phone: str | None = None
    bio: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    is_active: bool | None = None
    role: Literal["user", "admin"] | None = None


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    profile_pic: str
    security_answer: str
    social_media: dict
    phone: str
    bio: str
    date_of_birth: str
    address: str
    is_active: bool
    role: str
