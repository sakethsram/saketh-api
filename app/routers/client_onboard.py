from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import User
from app.models import EvenFlowAccountingDetails  # Import the EvenFlowAccountingDetails model
from app.schemas import EvenFlowAccountingDetailsSchema  # Import the schema for EvenFlowAccountingDetails
from app.security import validate_token  # Assuming you have a validate_token function

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/evenflow-accounting-details", response_model=List[EvenFlowAccountingDetailsSchema])
def get_evenflow_accounting_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),  # This uses HTTPBearer for current user validation
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Fetch all EvenFlow accounting details from the database.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)  # Validate the token with the provided function

    # Query all active EvenFlowAccountingDetails
    accounting_details = (
        db.query(EvenFlowAccountingDetails)
        .filter(EvenFlowAccountingDetails.active_flag == 1)
        .all()
    )

    if not accounting_details:
        raise HTTPException(status_code=404, detail="EvenFlow Accounting Details not found")

    # Return the result using the schema
    return [EvenFlowAccountingDetailsSchema.from_orm(detail) for detail in accounting_details]
