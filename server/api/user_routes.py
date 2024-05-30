# user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from core.logging_config import setup_logging
from db.database import get_db
from models.user import User
from schemas.user import UserCreate
from security.auth import get_current_user
from services.user_service import read_users_me, read_users, read_user, update_user, delete_user, delete_profile
from schemas.user import UserProfileUpdate
from services.user_service import create_profile, update_profile

logger = setup_logging()

router = APIRouter()


@router.get("/users/me/", tags=["Users"])
@cache(expire=60)  # Cache for 60 seconds
async def read_users_me_route(current_user: User = Depends(get_current_user)):
    return read_users_me(current_user)


@router.get("/users/", tags=["Users"])
@cache(expire=60)  # Cache for 60 seconds
async def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return read_users(skip, limit, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/{user_id}", tags=["Users"])
@cache(expire=60)  # Cache for 60 seconds
async def read_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        return read_user(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/users/{user_id}", tags=["Users"])
async def update_user_route(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    try:
        return update_user(user_id, user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/users/{user_id}", tags=["Users"])
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        return delete_user(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/current/", tags=["Users"])
async def get_current_user_route(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users/me/profile", tags=["Users"])
async def create_profile_route(profile: UserProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_profile(current_user.id, profile, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/users/me/profile", tags=["Users"])
async def update_profile_route(profile: UserProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return update_profile(current_user.id, profile, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/me/profile", tags=["Users"])
async def delete_profile_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return delete_profile(current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")






