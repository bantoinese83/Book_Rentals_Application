# models/book.py
from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    is_available = Column(Boolean, default=True)
    quantity = Column(Integer, default=1)  # New field for quantity
    book_lists = relationship("BookList", back_populates="book")
    rentals = relationship("Rental", back_populates="book")

    def __repr__(self):
        return (f"<Book(id={self.id}, title={self.title}, isbn={self.isbn},"
                f" is_available={self.is_available}, quantity={self.quantity})>")
