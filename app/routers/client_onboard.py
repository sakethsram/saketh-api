from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import ClientMaster, User
from app.schemas import ClientMasterSchema
from app.security import validate_token

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/get_clients", response_model=List[ClientMasterSchema])
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme), 
    authorization: str = Header(None, description="Bearer token for authentication")
    ):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db) 

    clients = db.query(ClientMaster).all()
    if not clients:raise HTTPException(status_code=404, detail="Clients not found")
    
    return [ClientMasterSchema(id=client.id,name=client.name) for client in clients]
    