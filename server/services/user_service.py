# user_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from schemas.user import UserCreate
from core.logging_config import setup_logging
from models.profile import Profile
from schemas.user import UserProfileUpdate

logger = setup_logging()


def read_users_me(current_user: User):
    return current_user


def read_users(skip: int, limit: int, db: Session):
    try:
        users = db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error reading users: {e}")
        raise
    return users


def read_user(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error reading user: {e}")
        raise
    if user is None:
        raise ValueError(f"User with id {user_id} not found")
    return user


def update_user(user_id: int, user: UserCreate, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError(f"User with id {user_id} not found")
        for var, value in vars(user).items():
            setattr(db_user, var, value) if value else None
        db.commit()
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error updating user: {e}")
        raise


def delete_user(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error deleting user: {e}")
        raise


def create_profile(user_id: int, profile: UserProfileUpdate, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError(f"User with id {user_id} not found")
        db_profile = Profile(**profile.dict(), user_id=user_id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except SQLAlchemyError as e:
        logger.error(f"Error creating profile: {e}")
        raise


def update_profile(user_id: int, profile: UserProfileUpdate, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError(f"User with id {user_id} not found")

        if db_user.profiles:
            db_profile = db_user.profiles[0]  # Get the first profile
        else:
            db_profile = Profile(user_id=user_id)  # Create a new profile
            db.add(db_profile)

        for var, value in profile.dict().items():
            if hasattr(db_profile, var) and value is not None:
                setattr(db_profile, var, value)

        db.commit()
        return db_profile
    except SQLAlchemyError as e:
        logger.error(f"Error updating profile: {e}")
        raise


def delete_profile(user_id: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError(f"User with id {user_id} not found")

        if db_user.profiles:
            db_profile = db_user.profiles[0]  # Get the first profile
            db.delete(db_profile)
            db.commit()
            return db_profile
        else:
            raise ValueError(f"Profile for user with id {user_id} not found")
    except SQLAlchemyError as e:
        logger.error(f"Error deleting profile: {e}")
        raise
