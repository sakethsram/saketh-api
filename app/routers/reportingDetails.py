from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.utils.logger  import logger
from app.helper.genericHelper import convertKeysToCamelCase
from datetime import date
from typing import List, Optional
from app.dependencies import get_db
from app.security import decode_access_token
from app.queries.reportingDetails import (
    GET_PURCHASE_ORDER_AGG_DETAILS,
    GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS,
    GET_INVOICES_TOP_CUSTOMERS_AGG_DETAILS,
    GET_INVOICES_AGG_DETAILS,
    GET_PO_COUNT_DETAILS,
    GET_PRICE_DETAILS_FOR_KPI
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
        logger.info("Request received for /getPurchaseOrderReportingDetails from-"+decoded_details.get('user_login_id'))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        poAggDetails = db.execute(text(GET_PURCHASE_ORDER_AGG_DETAILS)).mappings().all()
        poTopCustomersAggDetails = db.execute(text(GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS)).mappings().all()
        return {
            "poAggDetails": convertKeysToCamelCase(poAggDetails), 
            "poTopCustomersAggDetails": convertKeysToCamelCase(poTopCustomersAggDetails)
        }
    except Exception as e:
        logger.error(f"Failed to getPurchaseOrderReportingDetails: {e}")
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
        logger.info("Request received for /getInvoicesReportingDetails from-"+decoded_details.get('user_login_id'))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        invoicesAggDetails = db.execute(text(GET_INVOICES_AGG_DETAILS)).mappings().all()
        invoicesTopCustomersAggDetails = db.execute(text(GET_INVOICES_TOP_CUSTOMERS_AGG_DETAILS)).mappings().all()
        return {
            "invoicesAggDetails": convertKeysToCamelCase(invoicesAggDetails),
            "invoicesTopCustomersAggDetails": convertKeysToCamelCase(invoicesTopCustomersAggDetails)
        }
    except Exception as e:
        logger.error(f"Failed to getInvoicesReportingDetails: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getPoCountsForReporting")
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
        logger.info("Request received for /getPoCountsForReporting from-"+decoded_details.get('user_login_id'))
    except Exception as e:
        logger.error(f"Failed to getPoCountsForReporting: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        poCountDetails = db.execute(text(GET_PO_COUNT_DETAILS)).mappings().first()
        priceDetails = db.execute(text(GET_PRICE_DETAILS_FOR_KPI)).mappings().first()
        return {
            "poCountDetails": poCountDetails,
            "amountDetails": priceDetails
        }
    except Exception as e:
        logger.error(f"Failed to getPoCountsForReporting: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
        