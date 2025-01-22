from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models import User
from app.models import AccountingDetails
from app.schemas import AccountingDetailsSchema
from app.security import validate_token

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/account-details", response_model=List[AccountingDetailsSchema])
def get_accounting_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    accounting_details = (
        db.query(AccountingDetails)
        .filter(AccountingDetails.active_flag == 1)
        .all()
    )

    if not accounting_details:
        raise HTTPException(status_code=404, detail="Accounting Details not found")

    return [AccountingDetailsSchema(id=detail.id, name=detail.accounting_tool_name) for detail in accounting_details]
