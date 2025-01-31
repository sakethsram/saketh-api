import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
import shutil
import boto3
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, Header, Query, File, UploadFile, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.utils.logger  import logger
from app.helper.genericHelper import convertKeysToCamelCase
from datetime import date
from datetime import datetime
from typing import List, Optional
from app.dependencies import get_db
from app.security import validate_token
from app.models import User
import fitz
#from app.security import decode_access_token
from app.automationscript.poAutomation import ExtractPOData
from app.queries.po import (
    FETCH_PO_LISTING_QUERY,
    FETCH_TOTAL_COUNT_PO_LISTING_QUERY,
    PO_DETAILS_QUERY_BY_PO_NUMBER,
    PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITHOUT_FULFILLED,
    PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITH_FULFILLED
)
from app.queries.purchaseOrder import (
    INSERT_PURCHASE_ORDER_DETAILS,
    CHECK_PURCHASE_ORDER_EXIST
)
from app.queries.purchaseItemLineItem import (
    INSERT_PURCHASE_ORDER_LINE_ITEM
)
from app.queries.customer import (
    GET_CUSTOMER_ID_USING_CUSTOMER_NAME
)

load_dotenv()
router = APIRouter()
security_scheme = HTTPBearer()

class CreateInvoiceInputRequest(BaseModel):
    poNumber: str = Field(..., description="Purchase Order Number", example="PO12345")
    supplierName: str = Field(..., description="Name of the supplier", example="Acme Corp.")
    totalAmount: float = Field(..., ge=0, description="Total amount for the PO", example=1000.50)
    startDate: date = Field(..., description="Start date of the PO in YYYY-MM-DD format")
    endDate: Optional[date] = Field(None, description="End date of the PO in YYYY-MM-DD format")

class CreatePOLineItem(BaseModel):
    asin: str = Field(..., description="ASIN of the item", example="B0D95SFFL9")
    external_id: str = Field(..., description="External ID (e.g., EAN)", example="EAN:8906157936556")
    model_number: str = Field(..., description="Model number of the item", example="XTR-GM-GRY-P4")
    hsn: Optional[str] = Field(None, description="HSN code of the item", example="95049090")
    title: str = Field(..., description="Title/Description of the item", example="Xtrim Puzzle Exercise Mat")
    window_type: str = Field(..., description="Type of delivery window", example="Delivery window (Prepaid)")
    expected_date: str = Field(..., description="Expected delivery date", example="2024-11-21")
    quantity_requested: int = Field(..., description="Quantity requested", example=52)
    accepted_quantity: int = Field(..., description="Quantity accepted", example=52)
    quantity_received: int = Field(..., description="Quantity received", example=52)
    quantity_outstanding: int = Field(..., description="Outstanding quantity", example=0)
    unit_cost: str = Field(..., description="Unit cost in currency", example="533 INR")
    total_cost: str = Field(..., description="Total cost in currency", example="27716 INR")

class CreatePORequest(BaseModel):
    evenflow_customer_master_id: int = Field(..., description="customer master id", example=1)
    client_id: int = Field(..., description="ClientId", example=1)
    po_number: str = Field(..., description="Purchase Order number", example="7VTEZRNB")
    delivery_address_code: str = Field(..., description="Code of the delivery address", example="BLR4")
    delivery_address: str = Field(..., description="Full delivery address", example="RETAILEZ PRIVATE LIMITED\nPlot No. 12 P2, Hitech, Defence and Aerospace Park, Devanahalli\nBENGALURU 562149\nIndia")
    no_of_po_items: int = Field(..., description="Number of PO items", example=2)
    status: str = Field(..., description="Status of the PO", example="Closed")
    vendor: str = Field(..., description="Vendor code", example="EV7CR")
    ship_to_location: str = Field(..., description="Ship-to location", example="BLR4 - BENGALURU, KARNATAKA")
    ordered_on: str = Field(..., description="Order date", example="2024-11-20")
    ship_window: str = Field(..., description="Shipping window", example="21/11/2024 - 1/1/2025")
    freight_terms: str = Field(..., description="Freight terms", example="Prepaid")
    payment_method: str = Field(..., description="Payment method", example="Invoice")
    payment_terms: str = Field(..., description="Payment terms", example="NET DUE IN 45 DAYS")
    purchasing_entity: str = Field(..., description="Purchasing entity", example="RETAILEZ PRIVATE LIMITED")
    submitted_items: int = Field(..., description="Number of submitted items", example=2)
    submitted_quantity_submitted: int = Field(..., description="Total submitted quantity", example=82)
    submitted_total_cost: str = Field(..., description="Total cost of submitted items", example="37526.00 INR")
    accepted_items: int = Field(..., description="Number of accepted items", example=2)
    accepted_quantity_submitted: int = Field(..., description="Total accepted quantity", example=82)
    accepted_total_cost: str = Field(..., description="Total cost of accepted items", example="37526.00 INR")
    cancelled_items: int = Field(..., description="Number of cancelled items", example=0)
    cancelled_quantity_submitted: int = Field(..., description="Total cancelled quantity", example=0)
    cancelled_total_cost: str = Field(..., description="Total cost of cancelled items", example="0.00 INR")
    received_items: int = Field(..., description="Number of received items", example=2)
    received_quantity_submitted: int = Field(..., description="Total received quantity", example=82)
    received_total_cost: str = Field(..., description="Total cost of received items", example="37526.00 INR")
    po_line_items: List[CreatePOLineItem] = Field(..., description="List of line items in the PO")


@router.get("/poListing")
def list_po(
    pageSize: int = Query(10, description="Number of rows per page", ge=1),
    pageNumber: int = Query(1, description="Page number to fetch", ge=1),
    poNumber: Optional[str] = Query(None, description="Filter by PO Number"),
    startDate: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    endDate: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Fetch purchase order listing with filters.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    
    try:
        logger.info(f"Request received for /poListing from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    condition = ""
    if poNumber:
        condition += f" WHERE RESULT.po_number = '{poNumber}' "
    if startDate:
        condition += f"{'AND' if condition else 'WHERE'} RESULT.po_created >= '{startDate}' "
    if endDate:
        condition += f"{'AND' if condition else 'WHERE'} RESULT.po_created <= '{endDate}' "
    
    values = {"page_size": pageSize, "page_number": pageNumber, "whereCondition": condition}
    FETCH_PO_LISTING_QUERY_FORMATED = FETCH_PO_LISTING_QUERY.format(**values)
    FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED = FETCH_TOTAL_COUNT_PO_LISTING_QUERY.format(**values)

    try:
        result = db.execute(text(FETCH_PO_LISTING_QUERY_FORMATED)).mappings().all()
        totalRecords = db.execute(text(FETCH_TOTAL_COUNT_PO_LISTING_QUERY_FORMATED)).mappings().first()
    except Exception as e:
        logger.error(f"Failed to fetch poListing: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    return {
        "poRecordCount": totalRecords,
        "poRecords": convertKeysToCamelCase(result),
    }

@router.get("/poDetailsByPoNumber")
def get_po_details(
    poNumber: str = Query(..., description="PO Number to fetch details"),
    fulfilledItemRequired: int = Query(..., description="Completed Item Required to fetch details"),
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Fetch purchase order details and line items by PO Number.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(f"Request received for /poListing from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    values = {"po_number": poNumber}
    poDetailsQuery = PO_DETAILS_QUERY_BY_PO_NUMBER.format(**values)
    poLineItemDetailsQuery = ""
    if fulfilledItemRequired == 1:
        poLineItemDetailsQuery = PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITHOUT_FULFILLED.format(**values)
    else:
        poLineItemDetailsQuery = PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITH_FULFILLED.format(**values)

    try:
        poDetails = db.execute(text(poDetailsQuery)).mappings().first()
        poLineItemDetails = db.execute(text(poLineItemDetailsQuery)).mappings().all()
    except Exception as e:
        logger.error(f"Failed to get PO details: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    return {
        "poDetails": convertKeysToCamelCase(poDetails),
        "poLineItemDetails": convertKeysToCamelCase(poLineItemDetails),
    }


@router.post("/generatePoDetails", status_code=201, summary="Create new Purchase Orders") 
def generate_po_details(
    request: CreatePORequest,  # Accepts a list of objects
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here")
):
    """
    Insert po deatils and po line Item details.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received for /poListing from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    toalRequestedItems = 0
    for lineItem in request.po_line_items:
        toalRequestedItems = toalRequestedItems + lineItem.quantity_requested
    try:
        values = {"po_number": request.po_number}
        poDetailsQuery = CHECK_PURCHASE_ORDER_EXIST.format(**values)
        poDetails = db.execute(text(poDetailsQuery)).mappings().all()
        if poDetails:
            raise HTTPException(status_code=409, detail="PO Number already exist")

        formattedOrderedOn = datetime.strptime(request.ordered_on, "%m/%d/%Y").date()
        orderedOnMonth = formattedOrderedOn.month
        orderedOnYear = formattedOrderedOn.year
        orderedFiscalQuarter = ''
        if 4 <= orderedOnMonth <= 6:
            orderedFiscalQuarter = "Q1"
        elif 7 <= orderedOnMonth <= 9:
            orderedFiscalQuarter = "Q2"
        elif 10 <= orderedOnMonth <= 12:
            orderedFiscalQuarter = "Q3"
        else:  # January to March
            orderedFiscalQuarter = "Q4"

        shipWindowStartDate, shipWindowEndDate = request.ship_window.split(" - ")
        formattedShipWindowStartDate = datetime.strptime(shipWindowStartDate, "%d/%m/%Y").date().strftime("%Y-%m-%d")
        formattedShipWindowEndDate = datetime.strptime(shipWindowEndDate, "%d/%m/%Y").date().strftime("%Y-%m-%d")

        poDetailsInputDict = {
            'clientId': request.client_id,
            'evenflowCustomerMasterId': request.evenflow_customer_master_id,
            'toalRequestedItems': toalRequestedItems,
            'poNumber': request.po_number,
            'poStatus': request.status,
            'vendor': request.vendor,
            'shipToLocation': request.ship_to_location,
            'orderedOn': formattedOrderedOn.strftime("%Y-%m-%d"),
            'shipWindowFrom': formattedShipWindowStartDate,
            'shipWindowTo': formattedShipWindowEndDate,
            'freightTerms': request.freight_terms,
            'paymentMethod': request.payment_method,
            'paymentTerms': request.payment_terms,
            'purchasingEntity': request.purchasing_entity,
            'submittedItems': request.submitted_items,
            'submittedQty': request.submitted_quantity_submitted,
            'submittedTotalCost': float(request.submitted_total_cost.replace("INR", "").strip()),
            'acceptedItems': request.accepted_items,
            'acceptedQty': request.accepted_quantity_submitted,
            'acceptedTotalCost': float(request.accepted_total_cost.replace("INR", "").strip()),
            'cancelledItems': request.cancelled_items,
            'cancelledQty': request.cancelled_quantity_submitted,
            'cancelledTotalCost': float(request.cancelled_total_cost.replace("INR", "").strip()),
            'receivedItems': request.received_items,
            'receivedQty': request.received_quantity_submitted,
            'receivedTotalCost': float(request.received_total_cost.replace("INR", "").strip()),
            'deliveryAddressTo': request.delivery_address_code,
            'deliveryAddress': request.delivery_address,
            'fiscalQuarter': orderedFiscalQuarter,
            'poMonth': orderedOnMonth,
            'poYear': orderedOnYear,
            'activeFlag': 1,
            'createdBy': payload.get('user_login_id')
        }
        generate_po_query = text(INSERT_PURCHASE_ORDER_DETAILS)
        db.execute(generate_po_query, poDetailsInputDict)
        poDetails = db.execute(text(poDetailsQuery)).mappings().first()

        for lineItem in request.po_line_items:
            expectedDateFormatted = datetime.strptime(lineItem.expected_date, "%m/%d/%Y").date().strftime("%Y-%m-%d")
            poLineItemDetailsInputDict = {
                'evenflowPurchaseOrdersId': poDetails.id,
                'asin': lineItem.asin,
                'externalId': lineItem.external_id,
                'modelNumber': lineItem.model_number,
                'hsn': 0 if lineItem.hsn == "" else lineItem.hsn,
                'title': lineItem.title,
                'windowType': lineItem.window_type,
                'expectedDate': expectedDateFormatted,
                'qtyRequested': lineItem.quantity_requested,
                'qtyAccepted': lineItem.accepted_quantity,
                'qtyReceived': lineItem.quantity_received,
                'qtyOutstanding': lineItem.quantity_outstanding,
                'unitCost': float(lineItem.unit_cost.replace("INR", "").strip()),
                'totalCost': float(lineItem.total_cost.replace("INR", "").strip()),
                'activeFlag': 1,
                'createdBy': payload.get('user_login_id')
            }
            generate_po_line_item_query = text(INSERT_PURCHASE_ORDER_LINE_ITEM)
            db.execute(generate_po_line_item_query, poLineItemDetailsInputDict)

        db.commit()
        return {
            "message":  "PO Details inserted successfully"      
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to generatePoDetails: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")

@router.post("/uploadPo", status_code=200, summary="Upload Purchase Orders pdf file")
async def generate_po_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(..., description="Bearer token for authentication", example="Bearer your_token_here"),
    file: UploadFile = File(...),
    clientId: str = Form(...),
):
    """
    Insert po details and po line Item details and upload to S3.
    """
    MAX_FILE_SIZE = 10 * 1024 * 1024
    # Validate the authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(f"Request received for /poListing from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    if file.size > MAX_FILE_SIZE:
        logger.error(f"Failed to upload, file size exceeds the allowed limit of {MAX_FILE_SIZE / (1024 * 1024)} MB")
        raise HTTPException(status_code=400, detail="File size exceeds the allowed limit")
    
    # Validate file type
    if file.content_type != 'application/pdf':
        logger.error(f"Failed to uploadPo, Only PDF files are allowed")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    FOLDER_PATH = os.getenv("UPLOAD_FOLDER")
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    poFileLocation = os.path.join(FOLDER_PATH, file.filename)

    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    PO_MAPPING_FILE_S3_PATH = os.getenv("PO_MAPPING_FILE_S3_PATH")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    s3 = session.client('s3')
    mappingFilePath = os.path.join(FOLDER_PATH, "evenflow-po-mappings.csv")
    try:
        s3.download_file(AWS_BUCKET_NAME, PO_MAPPING_FILE_S3_PATH, mappingFilePath)
        print(f"Mapping file downloaded successfully to {mappingFilePath}")
    except Exception as e:
        logger.error(f"Failed to download, Error downloading file from S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading file from S3: {str(e)}")
    
    try:
        # Save the file to a local directory
        with open(poFileLocation, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to uploadPo, Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Need to supply the PO Mapping File path as well
    poData = ExtractPOData.get_data_from_po(poFileLocation, mappingFilePath)
    
    os.remove(poFileLocation)
    os.remove(mappingFilePath)
    poNumber = poData.get('po_number')
    
    try:
        buffer = BytesIO(await file.read()) 
        currentDate = datetime.now() 
        response = s3.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=f"evenflow/puchase-orders/"+currentDate.strftime('%Y-%m-%d')+"/evenflow-"+poNumber+"-"+str(currentDate)+".pdf", 
            Body=buffer,  
            ContentType=file.content_type, 
        )
    except Exception as e:
        logger.error(f"Failed to uploadPo, Error uploading file to S3: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {str(e)}")

    toalRequestedItems = 0
    for lineItem in poData.get("po_line_items"):
        toalRequestedItems = toalRequestedItems + int(lineItem.get('qty_requested'))
    try:
        values = {"po_number": poData.get('po_number')}
        poDetailsQuery = CHECK_PURCHASE_ORDER_EXIST.format(**values)
        poDetails = db.execute(text(poDetailsQuery)).mappings().all()
        if poDetails:
            raise HTTPException(status_code=409, detail="PO Number already exists")
        
        customerId = -1
        values = {"customer_name": poData.get('purchasing_entity')}
        customerDetailsQuery = GET_CUSTOMER_ID_USING_CUSTOMER_NAME.format(**values)
        customerDetails = db.execute(text(customerDetailsQuery)).mappings().first()
        if customerDetails:
            customerId = customerDetails.get('id')

        formattedOrderedOn = datetime.strptime(poData.get('ordered_on'), "%m/%d/%Y").date()
        orderedOnMonth = formattedOrderedOn.month
        orderedOnYear = formattedOrderedOn.year
        orderedFiscalQuarter = ''
        if 4 <= orderedOnMonth <= 6:
            orderedFiscalQuarter = "Q1"
        elif 7 <= orderedOnMonth <= 9:
            orderedFiscalQuarter = "Q2"
        elif 10 <= orderedOnMonth <= 12:
            orderedFiscalQuarter = "Q3"
        else:  # January to March
            orderedFiscalQuarter = "Q4"

        poDetailsInputDict = {
            'clientId': clientId,
            'evenflowCustomerMasterId': customerId,
            'toalRequestedItems': toalRequestedItems,
            'poNumber': poData.get('po_number'),
            'poStatus': poData.get('status'),
            'vendor': poData.get('vendor'),
            'shipToLocation': poData.get('ship_to_location'),
            'orderedOn': formattedOrderedOn.strftime("%Y-%m-%d"),
            'shipWindowFrom': poData.get('ship_window_from'),
            'shipWindowTo': poData.get('ship_window_to'),
            'freightTerms': poData.get('freight_terms'),
            'paymentMethod': poData.get('payment_method'),
            'paymentTerms': poData.get('payment_terms'),
            'purchasingEntity': poData.get('purchasing_entity'),
            'submittedItems': poData.get('submitted_items'),
            'submittedQty': poData.get('submitted_quantity_submitted'),
            'submittedTotalCost': float(poData.get('submitted_total_cost').replace("INR", "").strip()),
            'acceptedItems': poData.get('accepted_items'),
            'acceptedQty': poData.get('accepted_quantity_submitted'),
            'acceptedTotalCost': float(poData.get('accepted_total_cost').replace("INR", "").strip()),
            'cancelledItems': poData.get('cancelled_items'),
            'cancelledQty': poData.get('cancelled_quantity_submitted'),
            'cancelledTotalCost': float(poData.get('cancelled_total_cost').replace("INR", "").strip()),
            'receivedItems': poData.get('received_items'),
            'receivedQty': poData.get('received_quantity_submitted'),
            'receivedTotalCost': float(poData.get('received_total_cost').replace("INR", "").strip()),
            'deliveryAddressTo': poData.get('delivery_address_code'),
            'deliveryAddress': poData.get('delivery_address'),
            'fiscalQuarter': orderedFiscalQuarter,
            'poMonth': orderedOnMonth,
            'poYear': orderedOnYear,
            'activeFlag': 1,
            'createdBy': payload.get('user_login_id')
        }
        generate_po_query = text(INSERT_PURCHASE_ORDER_DETAILS)
        db.execute(generate_po_query, poDetailsInputDict)
        poDetails = db.execute(text(poDetailsQuery)).mappings().first()

        for lineItem in poData.get('po_line_items'):
            expectedDateFormatted = datetime.strptime(lineItem.get('expected_date'), "%m/%d/%Y").date().strftime("%Y-%m-%d")
            poLineItemDetailsInputDict = {
            'evenflowPurchaseOrdersId': poDetails.id,
            'externalId': lineItem.get('external_id'),
            'modelNumber': lineItem.get('model_number'),
            'hsn': lineItem.get('hsn') if lineItem.get('hsn') else None,  # Handle empty hsn
            'title': lineItem.get('title'),
            'windowType': lineItem.get('window_type'),
            'expectedDate': expectedDateFormatted,
            'qtyRequested': int(lineItem.get('qty_requested')) if lineItem.get('qty_requested').isdigit() else 0,  # Ensure qtyRequested is an integer
            'qtyAccepted': int(lineItem.get('qty_accepted')) if lineItem.get('qty_accepted').isdigit() else 0,  # Ensure qtyAccepted is an integer
            'qtyReceived': int(lineItem.get('qty_received')) if lineItem.get('qty_received').isdigit() else 0,  # Ensure qtyReceived is an integer
            'qtyOutstanding': int(lineItem.get('qty_outstanding')) if lineItem.get('qty_outstanding').isdigit() else 0,  # Ensure qtyOutstanding is an integer
            'unitCost': float(lineItem.get('unit_cost').replace("INR", "").strip()) if lineItem.get('unit_cost') else 0.0,  # Ensure unitCost is a float
            'totalCost': float(lineItem.get('total_cost').replace("INR", "").strip()) if lineItem.get('total_cost') else 0.0,  # Ensure totalCost is a float
            'activeFlag': 1,
            'createdBy': payload.get('user_login_id')
}
            generate_po_line_item_query = text(INSERT_PURCHASE_ORDER_LINE_ITEM)
            db.execute(generate_po_line_item_query, poLineItemDetailsInputDict)

        db.commit()
        return {
            "message":  "PO Details inserted successfully",
            "data": {
                "poNumber": poNumber
            }     
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to uploadPo, Error is: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again. error is:"+str(e))
