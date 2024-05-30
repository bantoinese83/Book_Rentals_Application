# auth.py
from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from db.database import get_db
from security.security import oauth2_scheme, ALGORITHM, SECRET_KEY, JWTError, ExpiredSignatureError
from models.user import User
from schemas.token import TokenData


# Dependency for getting the current user
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username or not isinstance(username, str):
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
