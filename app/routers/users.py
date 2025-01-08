from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import User
from app.schemas import UserSchema
from app.security import decode_access_token
import logging

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(get_db),
    authorization: str = Header(None, description="Bearer token for authentication", example="Bearer your_token_here")  # Add this
):
    """
    Fetch all users from the database where `active_flag` is 1.
    """
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    # Ensure the token is formatted correctly (if applicable)
    token_parts = authorization.split()
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")

    # Extract the actual token
    token = token_parts[1]
    decoded_data = decode_access_token(token)
    logging.debug(f"decoded_data :{decoded_data}")
    
    # Fetch all active users
    users = db.query(User).filter(User.active_flag == 1).all()
    if not users:
        raise HTTPException(status_code=404, detail="No active users found")
    return users
