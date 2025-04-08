# src/services/auth_service.py
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from BackEnd.src.core.config import settings
from BackEnd.src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from BackEnd.src.models.user import User
from BackEnd.src.schemas.user import TokenData, UserCreate
from BackEnd.src.database.database import get_db
from BackEnd.src.utils.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, user: UserCreate):
    try:
        # Check if username or email already exists
        if get_user_by_username(db, user.username):
            raise HTTPException(
                status_code=409, detail="Username already exists. Please log in."
            )
        if get_user_by_email(db, user.email):
            raise HTTPException(
                status_code=409, detail="Email already exists. Please log in."
            )

        hashed_password = get_password_hash(user.password)
        db_user = User(  # Make sure this is the ORM model from BackEnd.src.models.user
            email=user.email, username=user.username, hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user  # Ensure returning ORM model, not Pydantic schema
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during signup")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
