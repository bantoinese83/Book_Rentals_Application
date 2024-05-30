import secrets
import string
from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from models.user import User
from schemas.user import UserCreate
from security.security import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.renter import Renter

# Define the database session type
Session = Session


# Function for user registration
async def register(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, is_admin=False)
    db.add(db_user)
    db.commit()

    # Create a Renter record for the new user
    db_renter = Renter(user_id=db_user.id)
    db.add(db_renter)
    db.commit()

    return {"message": "User and renter created"}


async def register_admin(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, is_admin=True)
    db.add(db_user)
    db.commit()
    return {"message": "Admin created"}


# Function for user login
async def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Function for password reset
async def password_reset(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Generate a new random password
    new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
    # Hash the new password
    hashed_password = pwd_context.hash(new_password)
    # Update the user's password in the database
    user.hashed_password = hashed_password
    db.commit()
    # In a real application, the new password would be sent to the user's email
    return {"message": "Password reset successful", "new_password": new_password}
