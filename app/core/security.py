from datetime import datetime, timedelta, timezone
from typing import Any
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings


class SecurityManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def get_current_user(token: str = Depends(SecurityManager().oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security_manager.decode_token(token)
        username: str | None = payload.get("sub", None)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


security_manager = SecurityManager()
