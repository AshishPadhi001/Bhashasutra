# src/api/endpoints/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.user import User as UserModel
from src.schemas.user import User, UserUpdate
from src.services.auth_service import get_current_active_user
from src.core.security import get_password_hash
from src.utils.logger import logger

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Get the current logged-in user information
    """
    return current_user


@router.put("/me", response_model=User)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Update the current user's information
    """
    try:
        user_data = user_update.dict(exclude_unset=True)

        # If updating password, hash it
        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

        # Update user attributes
        for key, value in user_data.items():
            setattr(current_user, key, value)

        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user",
        )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Delete the current user
    """
    try:
        db.delete(current_user)
        db.commit()
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )
