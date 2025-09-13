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
    birthdate: date = Field(
        ..., description="User's birthdate in YYYY-MM-DD format", example="1990-01-01"
    )
    additional_info: Optional[str] = Field(
        None, max_length=255, description="Additional information about the user"
    )
