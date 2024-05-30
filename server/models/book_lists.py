# models/book_lists.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class BookList(Base):
    __tablename__ = "book_lists"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    renter_id = Column(Integer, ForeignKey('renters.id'))
    book = relationship("Book", back_populates="book_lists")
    renter = relationship("Renter", back_populates="book_lists")

    def __repr__(self):
        return f"<BookList(id={self.id}, book_id={self.book_id}, renter_id={self.renter_id})>"
