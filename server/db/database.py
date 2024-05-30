# database.py
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError

from db.database_config import SessionLocal


# Dependency for getting a DB session
def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        print(f"Error while connecting to DB: {e}")
    finally:
        if db is not None:
            db.close()
