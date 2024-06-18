# database_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all your models here
from models.user import User
from models.profile import Profile
from models.renter import Renter
from models.book import Book
from models.book_lists import BookList
from models.rental import Rental

from db.base import Base

DATABASE_URL = "postgresql://:@localhost:5432/_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the engine
Base.metadata.create_all(bind=engine)
