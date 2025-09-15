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

    # Allow creating this schema from SQLAlchemy model instances
    model_config = {
        "from_attributes": True,
    }
