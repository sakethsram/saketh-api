from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User, Role, UserRole
from app.security import create_access_token
from app.models import UserTokens
import jwt
import logging
from app.security import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Log database connection details
    engine = db.get_bind()
    database_url = str(engine.url)
    logging.debug(f"Connected to database: {database_url}, username: {username}")

    # Fetch user details by login ID
    user = db.query(User).filter(User.user_login_id == username, User.active_flag == 1).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    # Verify plain text password
    if password != user.user_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    # Fetch roles for the user
    user_roles = (
        db.query(Role.role_name)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user.id, UserRole.active_flag == 1, Role.active_flag == 1)
        .all()
    )
    
    roles = [role.role_name for role in user_roles]

    if not roles:
        raise HTTPException(
            status_code=403,
            detail="User has no assigned roles or roles are inactive.",
        )

    logging.debug(f"User: {user.user_first_name} {user.user_last_name}, Roles: {roles}, Client ID: {user.client_id}")

    # Check for existing valid token in the database
    existing_token_entry = db.query(UserTokens).filter(UserTokens.user_id == user.id).first()

    if existing_token_entry:
        try:
            # Decode and validate the existing token
            payload = jwt.decode(existing_token_entry.token, SECRET_KEY, algorithms=[ALGORITHM])
            logging.debug(f"Returning existing valid token for user {user.user_login_id}")
            return {
                "access_token": existing_token_entry.token,
                "token_type": "bearer",
                "roles": roles[0],
                "client_id": user.client_id,
                "user_full_name": f"{user.user_first_name} {user.user_last_name}",
            }
        except jwt.ExpiredSignatureError:
            logging.debug(f"Existing token for user {user.user_login_id} is expired, generating new token.")
            db.query(UserTokens).filter(UserTokens.user_id == user.id).delete()
            db.commit()

    # Generate a new access token
    access_token = create_access_token(data={
        "user_login_id": user.user_login_id,
        "roles": roles,
        "client_id": user.client_id
    })

    new_token_entry = UserTokens(
        user_id=user.id,
        token=access_token,
        created_by=user.id,
        modified_by=user.id,
        active_flag=1,
    )
    
    db.add(new_token_entry)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "roles": roles[0],
        "client_id": user.client_id,
        "user_full_name": f"{user.user_first_name} {user.user_last_name}",
    }
