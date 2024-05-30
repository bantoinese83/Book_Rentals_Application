from fastapi import Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic.fields import Field


class UserCreate(BaseModel):
    username: str = Form(...)
    password: str = Form(...)
    email: str = Form(...)


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="John Doe")
    bio: Optional[str] = Field(None, example="Software Developer at XYZ")
    avatar: Optional[str] = Field(None, example="https://example.com/avatar.jpg")
    location: Optional[str] = Field(None, example="San Francisco, CA")
    website: Optional[str] = Field(None, example="https://example.com")
    birth_date: Optional[datetime] = Field(None, example="1990-01-01T00:00:00Z")