# schemas/book.py
from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    isbn: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    isbn: Optional[str] = None


class BookInDB(BookBase):
    id: int
    is_available: bool
    quantity: int

    class Config:
        from_attributes = True
