from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import EvenflowDistys, EvenFlowAccountingDetails
from app.schemas import ClientOnboardingRequest
from app.security import validate_token
from datetime import datetime
import logging

router = APIRouter()

@router.post("/client_onboarding")
def client_onboarding(
    request: ClientOnboardingRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    client_id = payload['client_id']
    created_by = payload['user_login_id']
    modified_by = payload['user_login_id']
    isactive = 1

    logging.debug(f"Initial values set: client_id={client_id}, created_by={created_by}, \
                  modified_by={modified_by}, isactive={isactive}")

    # Insert multiple B2B distributors
    logging.debug("Processing B2B distributors")
    for disty in request.b2b_distributors:
        new_disty = EvenflowDistys(
            client_id=client_id,
            disty_id=disty.disty_id,
            created_on=datetime.utcnow(),
            created_by=created_by,
            modified_on=datetime.utcnow(),
            modified_by=modified_by,
            active_flag=isactive,
        )
        logging.debug(f"Prepared new_disty object: {vars(new_disty)}")
        db.add(new_disty)

    logging.debug("Processing accounting tool details")
    details = request.accounting_tool_details
    new_accounting_details = EvenFlowAccountingDetails(
        client_id=client_id,
        invoice_inputs=details.invoice_inputs,
        invoice_number_auto=details.invoice_number_auto,
        accounting_tool_name=details.accounting_tool_name,
        accounting_tool_url=details.accounting_tool_url,
        accounting_tool_userid=details.accounting_tool_userid,
        accounting_tool_pwd=details.accounting_tool_pwd,
        created_on=datetime.utcnow(),
        created_by=created_by,
        modified_on=datetime.utcnow(),
        modified_by=modified_by,
        active_flag=isactive,
    )
    logging.debug(f"Prepared new_accounting_details object: {vars(new_accounting_details)}")
    db.add(new_accounting_details)

    # Commit all changes
    logging.debug("Committing changes to the database")
    try:
        db.commit()
        logging.debug("Database commit successful")
    except Exception as e:
        logging.debug(f"Database commit failed: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to commit data to the database")

    return {"message": "Client onboarding data added successfully"}
