from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Renter(Base):
    __tablename__ = "renters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="renters")
    rentals = relationship("Rental", back_populates="renter")
    book_lists = relationship("BookList", back_populates="renter")

    def __repr__(self):
        return f"<Renter(id={self.id}, user_id={self.user_id})>"
