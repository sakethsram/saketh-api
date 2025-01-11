from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
from app.dependencies import get_db
from app.security import decode_access_token
from app.queries.po import FETCH_PO_LISTING_QUERY, FETCH_TOTAL_COUNT_PO_LISTING_QUERY

router = APIRouter()

@router.get("/poListing")
def list_users(
    pageSize: int = Query(10, description="Number of rows per page", ge=1),  # Default: 10, minimum value: 1
    pageNumber: int = Query(1, description="Page number to fetch", ge=1),   # Default: 1, minimum value: 1
    poNumber: str = Query(None, description="Page number to fetch"),
    startDate: str = Query(None, description="Start date filter"),
    endDate: str = Query(None, description="End date filter"),
    db: Session = Depends(get_db),
    authorization: str = Header(None, description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch purchase order and invoice details with raw SQL.
    """
    # Validate Authorization Header
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    
    # Parse the token
    token_parts = authorization.split()
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")

    token = token_parts[1]
    try:
        decoded_details = decode_access_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    condition = ""
    if poNumber:    
        condition =  " WHERE RESULT.po_number = '"+poNumber+"' "
    if startDate:
        if condition == "":
            condition = condition + " RESULT.po_created >= '"+startDate+"' "
        else:
            condition = condition + " AND RESULT.po_created >= '"+startDate+"' "
    if endDate:
        if condition == "":
            condition = condition + " RESULT.po_created <= '"+startDate+"' "
        else:
            condition = condition + " AND RESULT.po_created <= '"+endDate+"' "
        
    values = {"page_size": pageSize, "page_number": pageNumber, "whereCondition": condition}
    FETCH_PO_LISTING_QUERY_FORMATED = FETCH_PO_LISTING_QUERY.format(**values)
    FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED = FETCH_TOTAL_COUNT_PO_LISTING_QUERY.format(**values)
    try:
        result = db.execute(text(FETCH_PO_LISTING_QUERY_FORMATED)).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    try:
        totalRecords = db.execute(text(FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED)).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    return {
        "poRecordCount": totalRecords,
        "poRecords": result
    }