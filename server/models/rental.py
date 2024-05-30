from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base


class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    renter_id = Column(Integer, ForeignKey('renters.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rental_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime)
    renter = relationship("Renter", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")

    def __repr__(self):
        return (f"<Rental(id={self.id}, renter_id={self.renter_id}, book_id={self.book_id}, "
                f"rental_date={self.rental_date}"
                f", return_date={self.return_date})>")

