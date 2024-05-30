# models/profile.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profiles")
    full_name = Column(String)
    bio = Column(String)
    avatar = Column(String)
    location = Column(String)
    website = Column(String)
    birth_date = Column(DateTime)
    phone_number = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return (f"<Profile(id={self.id}, "
                f"user_id={self.user_id}, "
                f"full_name={self.full_name}, "
                f"bio={self.bio}, "
                f"avatar={self.avatar}, "
                f"location={self.location}, "
                f"website={self.website},"
                f" birth_date={self.birth_date}, "
                f"phone_number={self.phone_number}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")
