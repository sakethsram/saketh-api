from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import date
from typing import List, Optional
from app.dependencies import get_db
from app.security import decode_access_token
from app.queries.warehouse import (
    GET_WAREHOUSE_DETAILS
)

router = APIRouter()

@router.get("/getWarehouseList")
def get_warehouse_details(
    db: Session = Depends(get_db),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch warehouse details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    try:
        decoded_details = decode_access_token(authorization.split(" ")[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        result = db.execute(text(GET_WAREHOUSE_DETAILS)).mappings().all()
        return {
            "wareHouseList": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    