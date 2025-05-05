'''Authentication and password management.'''

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app import crud
from .database import get_database

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(database, username: str, password: str):
    '''
    Authenticate user,

        :param database: Database session.
        :param username: Username.
        :param password: Password.
        :return: The user.
    '''

    user = crud.get_user_by_username(database, username)
    if not user or not bcrypt.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict):
    '''
    Create access token,

        :param data: Data.
        :return: The token.
    '''

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), \
                        database: Session = Depends(get_database)):
    '''
    Get current user,

        :param token: session token.
        :param database: Database session.
        :return: The user.
    '''

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as jwt_error:
        raise credentials_exception from jwt_error
    user = crud.get_user_by_username(database, username)
    if user is None:
        raise credentials_exception
    return user
