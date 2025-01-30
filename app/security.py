from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from sqlalchemy.orm import Session
from app.models import UserTokens
from app.config.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str, db: Session):
    payload = None

    token_entry = db.query(UserTokens).filter(UserTokens.token == token).first()
    if not token_entry:
        raise HTTPException(status_code=403, detail="Login session expired or invalid session. Please log in again.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        db.query(UserTokens).filter(UserTokens.token == token).delete()
        db.commit()
        raise HTTPException(status_code=403, detail="Login session expired. Please log in again.")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid login session. Please log in again.")

    return payload
