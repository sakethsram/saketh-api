from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import User
from app.schemas import UserSchema
from app.security import validate_token
import logging

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(get_db),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Fetch all users from the database where `active_flag` is 1.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    
    # Fetch all active users
    users = db.query(User).filter(User.active_flag == 1).all()
    if not users:
        raise HTTPException(status_code=404, detail="No active users found")
    return users
