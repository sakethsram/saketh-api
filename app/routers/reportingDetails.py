from fastapi import APIRouter, Depends, HTTPException, Header, Query
from fastapi.security import HTTPBearer
from app.models import User
from app.security import validate_token
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.utils.logger  import logger
from app.helper.genericHelper import convertKeysToCamelCase
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Optional
from app.dependencies import get_db
#from app.security import decode_access_token
from app.queries.reportingDetails import (
    AGG_PURCHASE_ORDER_TOP_CUSTOMER,
    GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS,
    TOP_5_CUSTOMERS_BASED_ON_PO_COUNT,
    GET_INVOICES_AGG_DETAILS,
    GET_PO_COUNT_DETAILS,
    GET_PRICE_DETAILS_FOR_KPI,
    PO_TREND_CHART_DAILY_QUERY,
    PO_TREND_CHART_MONTHLY_QUERY,
    PO_TREND_CHART_QUARTERLY_QUERY,
    PO_TREND_CHART_YEARLY_QUERY,
    AGG_INVOICES_TOP_CUSTOMER,
    TOP_5_CUSTOMERS_BASED_ON_INVOICE_AMOUNT,
    TOP_5_CUSTOMERS_BASED_ON_INVOIVE_COUNT,
    GET_INVOICE_COUNT_DETAILS_FOR_KPI,
    GET_INVOICE_AMOUNT_DETAILS_FOR_KPI,
    INVOICE_TREND_CHART_DAILY_QUERY,
    INVOICE_TREND_CHART_MONTHLY_QUERY,
    INVOICE_TREND_CHART_QUARTERLY_QUERY,
    INVOICE_TREND_CHART_YEARLY_QUERY
)

from enum import Enum

class IntervalFilter(str, Enum):
    daily = "daily"
    monthly = "monthly"
    yearly = "yearly"
    quarterly = "quarterly"

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/getPurchaseOrderReportingDetails")
def get_warehouse_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch Purchase order reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(f"Request received for /getPurchaseOrderReportingDetails from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        top5CustomersBasedOnPOCount = db.execute(text(TOP_5_CUSTOMERS_BASED_ON_PO_COUNT)).mappings().all()
        top5CustomersBasedOnPOAmount = db.execute(text(GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS)).mappings().all()
        top5CustomersAggregatedPOAndAmountQtrOnQtr = db.execute(text(AGG_PURCHASE_ORDER_TOP_CUSTOMER)).mappings().all()
        return {
            "top5CustomersBasedOnPOCount": convertKeysToCamelCase(top5CustomersBasedOnPOCount), 
            "top5CustomersBasedOnPOAmount": convertKeysToCamelCase(top5CustomersBasedOnPOAmount),
            "top5CustomersAggregatedPOAndAmountQtrOnQtr": convertKeysToCamelCase(top5CustomersAggregatedPOAndAmountQtrOnQtr)
        }
    except Exception as e:
        logger.error(f"Failed to getPurchaseOrderReportingDetails: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getInvoiceReportingDetails")
def get_warehouse_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch invoices reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /getInvoicesReportingDetails from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        invoicesAggDetails = db.execute(text(AGG_INVOICES_TOP_CUSTOMER)).mappings().all()
        top5CustomersBasedOnInvoiceCount = db.execute(text(TOP_5_CUSTOMERS_BASED_ON_INVOIVE_COUNT)).mappings().all()
        top5CustomersBasedOnInvoiceAmount = db.execute(text(TOP_5_CUSTOMERS_BASED_ON_INVOICE_AMOUNT)).mappings().all()
        return {
            "invoicesAggDetails": convertKeysToCamelCase(invoicesAggDetails),
            "top5CustomersBasedOnInvoiceCount": convertKeysToCamelCase(top5CustomersBasedOnInvoiceCount),
            "top5CustomersBasedOnInvoiceAmount": convertKeysToCamelCase(top5CustomersBasedOnInvoiceAmount)
        }
    except Exception as e:
        logger.error(f"Failed to getInvoicesReportingDetails: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getPoCountsForReporting")
def get_warehouse_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch invoices reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /getPoCountsForReporting from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        poCountDetails = db.execute(text(GET_PO_COUNT_DETAILS)).mappings().first()
        priceDetails = db.execute(text(GET_PRICE_DETAILS_FOR_KPI)).mappings().first()
        return {
            "poCountDetails": convertKeysToCamelCase(poCountDetails),
            "amountDetails": convertKeysToCamelCase(priceDetails)
        }
    except Exception as e:
        logger.error(f"Failed to getPoCountsForReporting: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getPoTrendChartForReporting")
def get_warehouse_details(
    db: Session = Depends(get_db),
    intervalFilter: IntervalFilter = Query(..., description="Interval Filter", example = "daily"),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch trend chart reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /getPoTrendChartForReporting from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        endDate = datetime.today().date()
        startDate = datetime.today().date()
        poTrendChartQuery = ""
        if(intervalFilter == 'daily'):
            startDate = endDate - timedelta(days=30)
            values = {"startDate": startDate, "endDate": endDate }
            poTrendChartQuery = PO_TREND_CHART_DAILY_QUERY.format(**values)
        elif(intervalFilter == 'monthly'):
            startDate = endDate - relativedelta(months=24)
            values = {"startDate": startDate, "endDate": endDate }
            poTrendChartQuery = PO_TREND_CHART_MONTHLY_QUERY.format(**values)
        elif(intervalFilter == 'quarterly'):
            startDate = endDate - relativedelta(months=8*3)
            values = {"startDate": startDate, "endDate": endDate }
            poTrendChartQuery = PO_TREND_CHART_QUARTERLY_QUERY.format(**values)
        elif(intervalFilter == 'yearly'):
            startDate = endDate - relativedelta(years=5)
            values = {"startDate": startDate, "endDate": endDate }
            poTrendChartQuery = PO_TREND_CHART_YEARLY_QUERY.format(**values)
        
        aggregatedDataForTrendChart = db.execute(text(poTrendChartQuery)).mappings().all()
        
        return {
            "intervalFilter": convertKeysToCamelCase(intervalFilter),
            "data": convertKeysToCamelCase(aggregatedDataForTrendChart)
        }
    except Exception as e:
        logger.error(f"Failed to getPoTrendChartForReporting: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getInvoiceCountsForReporting")
def get_warehouse_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch invoices reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /getInvoiceCountsForReporting from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        InvoiceCountDetails = db.execute(text(GET_INVOICE_COUNT_DETAILS_FOR_KPI)).mappings().first()
        priceDetails = db.execute(text(GET_INVOICE_AMOUNT_DETAILS_FOR_KPI)).mappings().first()
        return {
            "InvoiceCountDetails": convertKeysToCamelCase(InvoiceCountDetails),
            "amountDetails": convertKeysToCamelCase(priceDetails)
        }
    except Exception as e:
        logger.error(f"Failed to getInvoiceCountsForReporting: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@router.get("/getInvoiceTrendChartForReporting")
def get_warehouse_details(
    db: Session = Depends(get_db),
    intervalFilter: IntervalFilter = Query(..., description="Interval Filter", example = "daily"),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch trend chart reporting details details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /getInvoiceTrendChartForReporting from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    try:
        endDate = datetime.today().date()
        startDate = datetime.today().date()
        InvoiceTrendChartQuery = ""
        if(intervalFilter == 'daily'):
            startDate = endDate - timedelta(days=30)
            values = {"startDate": startDate, "endDate": endDate }
            InvoiceTrendChartQuery = INVOICE_TREND_CHART_DAILY_QUERY.format(**values)
        elif(intervalFilter == 'monthly'):
            startDate = endDate - relativedelta(months=24)
            values = {"startDate": startDate, "endDate": endDate }
            InvoiceTrendChartQuery = INVOICE_TREND_CHART_MONTHLY_QUERY.format(**values)
        elif(intervalFilter == 'quarterly'):
            startDate = endDate - relativedelta(months=8*3)
            values = {"startDate": startDate, "endDate": endDate }
            InvoiceTrendChartQuery = INVOICE_TREND_CHART_QUARTERLY_QUERY.format(**values)
        elif(intervalFilter == 'yearly'):
            startDate = endDate - relativedelta(years=5)
            values = {"startDate": startDate, "endDate": endDate }
            InvoiceTrendChartQuery = INVOICE_TREND_CHART_YEARLY_QUERY.format(**values)
        
        aggregatedDataForTrendChart = db.execute(text(InvoiceTrendChartQuery)).mappings().all()
        
        return {
            "intervalFilter": convertKeysToCamelCase(intervalFilter),
            "data": convertKeysToCamelCase(aggregatedDataForTrendChart)
        }
    except Exception as e:
        logger.error(f"Failed to getInvoiceTrendChartForReporting: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")