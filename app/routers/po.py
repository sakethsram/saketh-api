from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import date
from typing import List, Optional
from app.dependencies import get_db
from app.security import decode_access_token
from app.queries.po import (
    FETCH_PO_LISTING_QUERY,
    FETCH_TOTAL_COUNT_PO_LISTING_QUERY,
    PO_DETAILS_QUERY_BY_PO_NUMBER,
    PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER,
)

router = APIRouter()

class CreateInvoiceInputRequest(BaseModel):
    poNumber: str = Field(..., description="Purchase Order Number", example="PO12345")
    supplierName: str = Field(..., description="Name of the supplier", example="Acme Corp.")
    totalAmount: float = Field(..., ge=0, description="Total amount for the PO", example=1000.50)
    startDate: date = Field(..., description="Start date of the PO in YYYY-MM-DD format")
    endDate: Optional[date] = Field(None, description="End date of the PO in YYYY-MM-DD format")


@router.get("/poListing")
def list_po(
    pageSize: int = Query(10, description="Number of rows per page", ge=1),  # Default: 10, minimum value: 1
    pageNumber: int = Query(1, description="Page number to fetch", ge=1),   # Default: 1, minimum value: 1
    poNumber: Optional[str] = Query(None, description="Filter by PO Number"),
    startDate: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    endDate: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch purchase order listing with filters.
    """
    # Validate Authorization Header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    # Decode token
    try:
        decoded_details = decode_access_token(authorization.split(" ")[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    # Build WHERE conditions
    condition = ""
    if poNumber:
        condition += f" WHERE RESULT.po_number = '{poNumber}' "
    if startDate:
        condition += f"{'AND' if condition else 'WHERE'} RESULT.po_created >= '{startDate}' "
    if endDate:
        condition += f"{'AND' if condition else 'WHERE'} RESULT.po_created <= '{endDate}' "
    
    # Prepare queries
    values = {"page_size": pageSize, "page_number": pageNumber, "whereCondition": condition}
    FETCH_PO_LISTING_QUERY_FORMATED = FETCH_PO_LISTING_QUERY.format(**values)
    FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED = FETCH_TOTAL_COUNT_PO_LISTING_QUERY.format(**values)

    try:
        result = db.execute(text(FETCH_PO_LISTING_QUERY_FORMATED)).mappings().all()
        totalRecords = db.execute(text(FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED)).mappings().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    return {
        "poRecordCount": totalRecords,
        "poRecords": result,
    }


@router.get("/poDetailsByPoNumber")
def get_po_details(
    poNumber: str = Query(..., description="PO Number to fetch details"),
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch purchase order details and line items by PO Number.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    try:
        decoded_details = decode_access_token(authorization.split(" ")[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    values = {"po_number": poNumber}
    poDetailsQuery = PO_DETAILS_QUERY_BY_PO_NUMBER.format(**values)
    poLineItemDetailsQuery = PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER.format(**values)

    try:
        poDetails = db.execute(text(poDetailsQuery)).mappings().first()
        poLineItemDetails = db.execute(text(poLineItemDetailsQuery)).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    return {
        "poDetails": poDetails,
        "poLineItemDetails": poLineItemDetails,
    }
