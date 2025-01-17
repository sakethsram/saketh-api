from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import DistyMaster  # Import the DistyMaster model
from app.schemas import DistyMasterSchema  # Import the schema for DistyMaster
from app.security import validate_token  # Assuming you have a validate_token function

router = APIRouter()

@router.get("/distys", response_model=List[DistyMasterSchema])
def get_distys(
    db: Session = Depends(get_db),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Fetch all distys from the database.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)  # Validate the token (you should have this function)

    # Fetch all distys
    distys = db.query(DistyMaster.id, DistyMaster.name).all()  # Query all distys
    if not distys:
        raise HTTPException(status_code=404, detail="Distys not found")
    return [DistyMasterSchema(id=disty.id, name=disty.name) for disty in distys]
