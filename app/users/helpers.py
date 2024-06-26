import json

from app.db.database import engine, SessionLocal
from typing import Union, Any, List, Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.users.models import User
from app.users.schemas import UserOut, TokenPayload
from app.helpers import get_db
import os
from app.config import get_config
import jwt

settings = get_config(config=os.getenv("env") or 'dev')

from sqlalchemy.ext.declarative import DeclarativeMeta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def sqlalchemy_to_json(obj):
    """
    Convert a SQLAlchemy model object to JSON.
    """
    if isinstance(obj.__class__, DeclarativeMeta):
        # If the object is a SQLAlchemy model, extract its attributes
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    else:
        # If the object is not a SQLAlchemy model, raise an error
        raise TypeError("Object is not a SQLAlchemy model")


def create_access_token(subject: Union[str, Any], roles: List[int], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        print("expire time - ", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "roles": roles}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], roles: List[int], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "roles": roles}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode and verify the token
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        # Optionally, you can perform additional validation checks here
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Token signature is invalid")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)) -> UserOut:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        print(datetime.fromtimestamp(token_data.exp), "expiry time", datetime.utcnow())
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Token signature is invalid")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = db.query(User).filter(User.email == token_data.sub).one()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    user = sqlalchemy_to_json(user)
    return UserOut(**user)