from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from app.models import User
from app.security import validate_token
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.utils.logger  import logger
from datetime import date
from typing import List, Optional
from app.dependencies import get_db
#from app.security import decode_access_token
from app.queries.customer import (
    GET_CUSTOMER_DETAILS
)
from app.queries.productMaster import (
    GET_PRODUCT_DETAILS
)
from app.queries.purchaseOrder import (
    GET_PURCHASE_ORDER_DETAILS,
    UPDATE_PURCHASE_ORDER_DETAILS
)
from app.queries.accountingDetails import (
    GET_ACCOUNTING_DETAILS
)
from app.queries.purchaseItemLineItem import (
    GET_PURCHASE_ORDER_LINE_ITEM,
    UPDATE_PURCHASE_ORDER_LINE_ITEM
)
from app.queries.invoieInput import (
    CREATE_INVOICE_INPUT
)

router = APIRouter()
security_scheme = HTTPBearer()


# Pydantic Model for each item
class CreateInvoiceInputRequest(BaseModel):
    clientId: int = Field(..., description="Client Id", example=1)
    customerMasterId: int = Field(..., description="Customer master Id", example=1)
    poNumber: str = Field(..., description="Purchase Order Number", example="PO12345")
    poLineItemId: int = Field(..., description="po line item id", example = 1)
    ASIN:  str = Field(..., description="ASIN", example="ASIN number")
    sku: str = Field(..., description="SKU", example="SKU number")
    appointmentId: int = Field(..., description="appoinment id", example=101)
    appointmentDate: date = Field(..., description="appintment date", example="2025=01-01")
    acceptedQty: int = Field(..., description="Accepted quantity", example=10)
    placeOfSupply: Optional[str] = Field(None, description="Place of suply", example="Bangalore")
    totalBoxCount: int = Field(..., description="Total Box count", example=10)
    boxNumber: str = Field(..., description="Box Numbetr", example="box number")
    notes: str = Field(..., description="Notes", example="any comment")
    supplierName: str = Field(..., description="Name of the supplier", example="Acme Corp.")

    otherWarehouseName: Optional[str] = Field(None, description="Other Warehouse Name", example="xyz")
    otherWarehouseAddressLine1: Optional[str] = Field(None, description="Other Warehouse AddressLine1", example="xyz")
    otherWarehouseAddressLine2: Optional[str] = Field(None, description="Other Warehouse AddressLine2", example="xyz")
    otherWarehouseCity: Optional[str] = Field(None, description="other Warehouse City", example="xyz")
    otherWarehouseState: Optional[str] = Field(None, description="other Warehouse State", example="xyz")
    otherWarehouseCountry: Optional[str] = Field(None, description="other Warehouse Country", example="xyz")
    otherWarehousePostalCode: Optional[str] = Field(None, description="other Warehouse Postal Code", example="xyz")

# Updated endpoint for handling an array of objects
@router.post("/generateInvoiceInputs", status_code=201, summary="Create new Invoice input")
def create_invoice_input(
    requests: List[CreateInvoiceInputRequest],  # Accepts a list of objects
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Create new Invoice input from an array of input objects.
    """
    # Validate authorization
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(f"Request received for /poListing from - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    allOrderQtySatisfiedFlag = "FULFILLED"
    purchaseOrderNumber = ""
    # Process each request in the input list
    try:
        for request in requests:
            purchaseOrderNumber = request.poNumber
            values = {"customer_id": request.customerMasterId}
            GET_CUSTOMER_DETAILS_FORMATED = GET_CUSTOMER_DETAILS.format(**values)
            customerInfo = db.execute(text(GET_CUSTOMER_DETAILS_FORMATED)).mappings().first()
            values = {"sku": request.sku}
            GET_PRODUCT_DETAILS_FORMATED = GET_PRODUCT_DETAILS.format(**values)
            productInfo = db.execute(text(GET_PRODUCT_DETAILS_FORMATED)).mappings().first()
            if not productInfo:
                logger.error(f"Product details not found for the sku {request.sku}")
                raise HTTPException(status_code=404, detail=f"Product details not found for the sku {request.sku}")
            values = {"po_number": request.poNumber}
            GET_PURCHASE_ORDER_DETAILS_FORMATTED = GET_PURCHASE_ORDER_DETAILS.format(**values) 
            purchaseOrderDetails = db.execute(text(GET_PURCHASE_ORDER_DETAILS_FORMATTED)).mappings().first()
            # Fetching accounting details for the given clientId
            logger.info(f"Fetching accounting details for clientId {request.clientId}")
            values = {"client_id": request.clientId}
            GET_ACCOUNTING_DETAILS_FORMATTED = GET_ACCOUNTING_DETAILS.format(**values)
            accountingDetails = db.execute(text(GET_ACCOUNTING_DETAILS_FORMATTED)).mappings().first()

            # Log the accounting details result
            logger.info(f"Accounting details for clientId {request.clientId}: {accountingDetails}")
            
            if not accountingDetails:
                logger.error(f"Accounting details not found for clientId {request.clientId}")
                raise HTTPException(status_code=404, detail=f"Accounting details not found for clientId {request.clientId}")
            
            values = {'purchase_order_line_item_id': request.poLineItemId}
            GET_PURCHASE_ORDER_LINE_ITEM_FORMATTED = GET_PURCHASE_ORDER_LINE_ITEM.format(**values) 
            purchaseOrderLineItemDetails = db.execute(text(GET_PURCHASE_ORDER_LINE_ITEM_FORMATTED)).mappings().first()
            
            # Check if purchaseOrderLineItemDetails is None
            if purchaseOrderLineItemDetails is None:
                logger.error(f"Purchase order line item not found with po line item id  {request.poLineItemId}")
                raise HTTPException(status_code=404, detail=f"Purchase order line item not found with po line item id {request.poLineItemId}")

            orderedDate = purchaseOrderDetails.ordered_on

            lineItemQtySatisfy = 'FULFILLED'
            if request.acceptedQty != purchaseOrderLineItemDetails.quantity:
                lineItemQtySatisfy = "PARTIALLY_FULFILLED"
                allOrderQtySatisfiedFlag = "PARTIALLY_FULFILLED"
            orderedFiscalQuarter = ''
            if 4 <= orderedDate.month <= 6:
                orderedFiscalQuarter = "Q1"
            elif 7 <= orderedDate.month <= 9:
                orderedFiscalQuarter = "Q2"
            elif 10 <= orderedDate.month <= 12:
                orderedFiscalQuarter = "Q3"
            else:  # January to March
                orderedFiscalQuarter = "Q4"
            
            invoiceInputDict = {
                'clientId': request.clientId,
                'evenflowCustomerMasterId': request.customerMasterId,
                'evenflowProductMasterId': productInfo.id,
                'invoiceStatus': 'NOT_RAISED',
                'customerName': customerInfo.customer_name,
                'gstTreatment': customerInfo.gst_treatment,
                'tcsTaxName': customerInfo.tax_name,
                'tcsPercentage': customerInfo.tax_percentage,
                'gstin': customerInfo.gst_identification_number,
                'placeOfSupply': request.placeOfSupply,
                'poNumber': request.poNumber,
                'poLineItemId': request.poLineItemId, #added by Ikshwak jan 31st
                'evenflowPurchaseOrdersId': purchaseOrderDetails.evenflow_purchase_orders_id,
                'paymentTerms': customerInfo.payment_terms,
                'paymentTermsLabel': customerInfo.payment_terms_label,
                'expectedDate': purchaseOrderLineItemDetails.expected_date,
                'account': productInfo.account,
                'itemName': productInfo.item_name,
                'sku': request.sku,
                'itemDesc': productInfo.description,
                'itemType': productInfo.product_type,
                'hsnSac': productInfo.hsn_sac,
                'quantity': purchaseOrderLineItemDetails.quantity,
                'usageUnit': productInfo.usage_unit,
                'itemPrice': productInfo.rate,
                'itemTaxExemptionReason': productInfo.exemption_reason,
                'isInclusiveTax': productInfo.is_inclusive_tax,
                'itemTax': productInfo.intra_state_tax_name,
                'itemTaxType': productInfo.intra_state_tax_type,
                'itemTaxPercentage': productInfo.intra_state_tax_rate,
                'notes': request.notes,
                'fiscalQuarter': orderedFiscalQuarter,
                'poMonth': orderedDate.month,
                'poYear': orderedDate.year,
                'appointmentId': request.appointmentId,
                'appointmentDate': request.appointmentDate,
                'acceptedQty': request.acceptedQty,
                'invoiceGeneratedAccTool': accountingDetails.accounting_tool_id,
                'poFilePath': purchaseOrderDetails.po_file_path,
                'boxNumber': request.boxNumber,
                'totalBoxCount': request.totalBoxCount,
                'activeFlag': 1,
                'createdBy': payload.get('user_login_id'),
                'otherWarehouseName': request.otherWarehouseName,
                'otherWarehouseAddressLine1': request.otherWarehouseAddressLine1,
                'otherWarehouseAddressLine2': request.otherWarehouseAddressLine2,
                'otherWarehouseCity': request.otherWarehouseCity,
                'otherWarehouseState': request.otherWarehouseState,
                'otherWarehouseCountry': request.otherWarehouseCountry,
                'otherWarehousePostalCode': request.otherWarehousePostalCode,
                'poLineItemProcessingStatus': lineItemQtySatisfy
            }
            new_po_query = text(CREATE_INVOICE_INPUT)
            db.execute(new_po_query, invoiceInputDict)

            values = {'purchase_orders_id': purchaseOrderDetails.evenflow_purchase_orders_id, 'sku': request.sku, 'po_status': lineItemQtySatisfy}
            UPDATE_PURCHASE_ORDER_LINE_ITEM_FORMATTED = UPDATE_PURCHASE_ORDER_LINE_ITEM.format(**values)
            db.execute(text(UPDATE_PURCHASE_ORDER_LINE_ITEM_FORMATTED))

        values = { 'po_number': purchaseOrderNumber, 'po_status': allOrderQtySatisfiedFlag }
        UPDATE_PURCHASE_ORDER_DETAILS_FORMATTED = UPDATE_PURCHASE_ORDER_DETAILS.format(**values)
        db.execute(text(UPDATE_PURCHASE_ORDER_DETAILS_FORMATTED))

        db.commit()
        return {"message": "Invoice line item created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create invoice Order {request.poNumber}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create invoice Order {request.poNumber}: {str(e)}")

    
