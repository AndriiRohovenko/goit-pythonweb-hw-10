from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional


class UserSchema(BaseModel):
    name: str = Field(
        ..., max_length=50, description="User's first name", example="John"
    )
    surname: str = Field(
        ..., max_length=50, description="User's surname", example="Doe"
    )
    email: EmailStr = Field(
        ...,
        max_length=100,
        description="User's email address",
        example="john.doe@example.com",
    )

    model_config = {
        "from_attributes": True,
    }


class UserUploadAvatarSchema(BaseModel):
    avatar: Optional[str] = Field(
        None,
        description="URL of the user's avatar image",
        example="https://example.com/avatars/johndoe.jpg",
    )
