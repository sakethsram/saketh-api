from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import date
from typing import List, Optional
from app.dependencies import get_db
from app.security import decode_access_token
from app.queries.reportingDetails import (
    GET_PURCHASE_ORDER_AGG_DETAILS,
    GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS,
    GET_INVOICES_TOP_CUSTOMERS_AGG_DETAILS,
    GET_INVOICES_AGG_DETAILS
)

router = APIRouter()

@router.get("/getPurchaseOrderReportingDetails")
def get_warehouse_details(
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch Purchase order reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    try:
        decoded_details = decode_access_token(authorization.split(" ")[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        poAggDetails = db.execute(text(GET_PURCHASE_ORDER_AGG_DETAILS)).mappings().all()
        poTopCustomersAggDetails = db.execute(text(GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS)).mappings().all()
        return {
            "poAggDetails": poAggDetails,
            "poTopCustomersAggDetails": poTopCustomersAggDetails
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getInvoicesReportingDetails")
def get_warehouse_details(
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch invoices reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    try:
        decoded_details = decode_access_token(authorization.split(" ")[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        invoicesAggDetails = db.execute(text(GET_INVOICES_AGG_DETAILS)).mappings().all()
        invoicesTopCustomersAggDetails = db.execute(text(GET_INVOICES_TOP_CUSTOMERS_AGG_DETAILS)).mappings().all()
        return {
            "invoicesAggDetails": invoicesAggDetails,
            "invoicesTopCustomersAggDetails": invoicesTopCustomersAggDetails
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    