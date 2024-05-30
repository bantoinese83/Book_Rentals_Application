# security.py
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

# Initialize password hasher
pwd_context = CryptContext(schemes=["argon2", "scrypt"], deprecated="auto")

# Initialize OAuth2 with password (and hashing) a scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key for JWT creation - this should be hidden and in a secure place
SECRET_KEY = "154e94c6dd6f6f5780a8001988bf306047814576bf0e7901827762548e161a0b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # One year


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        return ""


class JWTError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ExpiredSignatureError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
