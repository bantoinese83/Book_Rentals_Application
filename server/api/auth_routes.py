from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.user import UserCreate
from services import auth_service

router = APIRouter()


# Endpoint for user registration
@router.post("/register", tags=["Authentication"])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await auth_service.register(user, db)


@router.post("/register_admin", tags=["Authentication"])
async def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    return await auth_service.register_admin(user, db)


# Endpoint for login
@router.post("/token", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await auth_service.login(form_data, db)


# Endpoint for password reset
@router.post("/password_reset/{email}", tags=["Authentication"])
async def password_reset(email: str, db: Session = Depends(get_db)):
    return await auth_service.password_reset(email, db)
