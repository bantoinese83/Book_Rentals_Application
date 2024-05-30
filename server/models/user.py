# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from models.profile import Profile  # Make sure to import the Profile class


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    date_joined = Column(DateTime)
    profiles = relationship("Profile", back_populates="user")
    renters = relationship("Renter", back_populates="user")

    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username}, email={self.email}, first_name={self.first_name}, "
                f"last_name={self.last_name}, is_active={self.is_active}, is_admin={self.is_admin}, date"
                f"_joined={self.date_joined})>")
