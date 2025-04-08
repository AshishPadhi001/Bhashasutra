# src/api/endpoints/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from BackEnd.src.core.config import settings
from BackEnd.src.database.database import get_db
from BackEnd.src.schemas.user import Token, UserCreate, User
from BackEnd.src.services.auth_service import (
    authenticate_user,
    create_user,
    create_access_token,
    get_current_active_user,
)
from BackEnd.src.services.email_service import EmailService
from BackEnd.src.utils.logger import logger
from BackEnd.src.models.user import (
    User as UserModel,
)  # Import the actual model with a different name

router = APIRouter(prefix="/auth", tags=["Authentication"])
email_service = EmailService()


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.
    """
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the database by their email.
    """
    return db.query(UserModel).filter(UserModel.email == email).first()


def send_welcome_email_background(email: str, username: str):
    """Background task to send welcome email"""
    email_service.send_welcome_email(email, username)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new user with the provided username, email, and password.
    """
    try:
        # Check if username exists
        existing_username = (
            db.query(UserModel).filter(UserModel.username == user_data.username).first()
        )

        # Check if email exists
        existing_email = (
            db.query(UserModel).filter(UserModel.email == user_data.email).first()
        )

        # Handle the different cases
        if existing_username and existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both username and email already exist",
            )
        elif existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Try any other username"
            )
        elif existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        # Create the user if no conflicts exist
        db_user = create_user(db, user_data)

        # Add email sending as background task
        background_tasks.add_task(
            send_welcome_email_background, db_user.email, db_user.username
        )

        return User(  # Ensure response matches Pydantic schema
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during signup")


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Get an access token using username and password
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
            "email": user.email,
        }
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login",
        )
