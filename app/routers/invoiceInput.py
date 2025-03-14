from datetime import date
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.dependencies import get_db
from app.models import User
from app.queries.accountingDetails import GET_ACCOUNTING_DETAILS
from app.queries.clientMaster import GET_CLIENT_DETAILS

#from app.security import decode_access_token
from app.queries.customer import GET_CUSTOMER_DETAILS
from app.queries.invoieInput import CREATE_INVOICE_INPUT
from app.queries.invoieInput import GET_MAX_ITERATION_NUMBER
from app.queries.invoieInput import UPDATE_PROCESSING_STATUS
from app.queries.invoieInput import UPDATE_TAX_COLUMNS
from app.queries.productMaster import GET_PRODUCT_DETAILS
from app.queries.purchaseItemLineItem import GET_PURCHASE_ORDER_LINE_ITEM
from app.queries.purchaseItemLineItem import UPDATE_PURCHASE_ORDER_LINE_ITEM
from app.queries.purchaseOrder import GET_PURCHASE_ORDER_DETAILS
from app.queries.purchaseOrder import UPDATE_PURCHASE_ORDER_DETAILS
from app.security import validate_token
from app.utils.logger import logger

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
    appointmentId: str = Field(..., description="appoinment id", example=101)
    appointmentDate: date = Field(..., description="appintment date", example="2025=01-01")
    fulfilledQty: int = Field(..., description="Fulfilled quantity", example=10)
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

    # billingAttention: Optional[str] = Field(None, description="Billing Attention", example="xyz")
    # billingAddressLine1: Optional[str] = Field(None, description="Billing Address Line1", example="xyz")
    # billingAaddressLine2: Optional[str] = Field(None, description="Billing Address Line", example="xyz")
    # billingCity: Optional[str] = Field(None, description="billing City", example="xyz")
    # billingState: Optional[str] = Field(None, description="billing State", example="xyz")        
    # billingCountry: Optional[str] = Field(None, description="billing Country", example="xyz")      
    # billingCode: Optional[str] = Field(None, description="billing Code", example="xyz")         
    # billingPhone: Optional[str] = Field(None, description="billing Phone", example="xyz")        
    # billingFax: Optional[str] = Field(None, description="billing Fax", example="xyz")          
    # shippingAttention: Optional[str] = Field(None, description="shipping Attention", example="xyz")   
    # shippingAddressLine1: Optional[str] = Field(None, description="shipping Address Line1", example="xyz")
    # shippingAddressLine2: Optional[str] = Field(None, description="shipping Address Line2", example="xyz")
    # shippingCity: Optional[str] = Field(None, description="shipping City", example="xyz")        
    # shippingState: Optional[str] = Field(None, description="shipping State", example="xyz")       
    # shippingCountry: Optional[str] = Field(None, description="shipping Country", example="xyz")     
    # shippingCode: Optional[str] = Field(None, description="shipping Code", example="xyz")        
    # shippingPhone: Optional[str] = Field(None, description="shipping Phone", example="xyz")       
    # shippingFax: Optional[str] = Field(None, description="shipping Fax", example="xyz")         
    # bankName: Optional[str] = Field(None, description="bank Name", example="xyz")
    # bankAccountNumber: int = Field(None, description="bank Account Number", example=28)
    # ifsc: Optional[str] = Field(None, description="ifsc", example="xyz")
    # accountType: Optional[str] = Field(None, description="account Type")

    # #added new columns by dheeraj
    # brandName: Optional[str] = Field(None,description="brand Name",example="xyz")  
    # brandPan:Optional[str] = Field(None,description="brand Pan",example="xyz") 
    # brandGstin:Optional[str] = Field(None,description="brand Gstin",example="xyz") 
    # brandRegAddressLine1:Optional[str] = Field(None,description="brand Reg Address Line 1",example="xyz")  
    # brandRegAddressLine2: Optional[str] = Field(None, description="brand Reg Address Line 2", example="xyz")
    # brandRegCity: Optional[str] = Field(None, description="brand Reg City", example="xyz")
    # brandRegState: Optional[str] = Field(None, description="brand Reg State", example="xyz")
    # brandRegCountry: Optional[str] = Field(None, description="brand Reg Country", example='xyz')
    # cgstPercentage: Optional[int] = Field(..., description="cgst Percentage", example=6)
    # cgstAmount: Optional[int] = Field(..., description="cgst Amount", example=6)
    # sgstPercentage: Optional[int] = Field(..., description="sgst Percentage", example=6)
    # sgstAmount: Optional[int] = Field(..., description="sgst Amount", example=6)
    # igstPercentage: Optional[int] = Field(..., description="igst Percentage", example=6)
    # igstAmount: Optional[int] = Field(..., description="igst_amount", example=6)
    # amount: Optional[int] = Field(..., description="amount", example=6)
 

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

    iterationIdFlag = True
    purchaseOrderNumber = ""
    iterationNumber = 1
    try:
        for request in requests:
            purchaseOrderNumber = request.poNumber
            if iterationIdFlag:
                values = { "poNumber": purchaseOrderNumber }
                GET_MAX_ITERATION_NUMBER_FORMATED = GET_MAX_ITERATION_NUMBER.format(**values)
                maxIterationNumber = db.execute(text(GET_MAX_ITERATION_NUMBER_FORMATED)).mappings().first()
                if(maxIterationNumber and maxIterationNumber.iteration_id):
                    iterationNumber = maxIterationNumber.iteration_id + 1
                iterationIdFlag = False

            values = {"client_id": request.clientId }
            GET_CLIENT_MASTER_DETAILS_FORMATED = GET_CLIENT_DETAILS.format(**values)
            clientInfo = db.execute(text(GET_CLIENT_MASTER_DETAILS_FORMATED)).mappings().first()
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
                'quantity': request.fulfilledQty,
                'usageUnit': productInfo.usage_unit,
                'itemPrice': productInfo.rate,
                'itemTaxExemptionReason': productInfo.exemption_reason,
                'isInclusiveTax': productInfo.is_inclusive_tax,
                
                'notes': request.notes,
                'fiscalQuarter': orderedFiscalQuarter,
                'poMonth': orderedDate.month,
                'poYear': orderedDate.year,
                'appointmentId': request.appointmentId,
                'appointmentDate': request.appointmentDate,
                'acceptedQty': purchaseOrderLineItemDetails.quantity,
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
                'modifiedBy': payload.get('user_login_id'),
                'iterationNumber': iterationNumber,
                #-----
                'billingAttention': customerInfo.billing_attention,
                'billingAddressLine1': customerInfo.billing_address_line_1 ,
                'billingAaddressLine2': customerInfo.billing_address_line_2 ,
                'billingCity': customerInfo.billing_city ,
                'billingState': customerInfo.billing_state ,
                'billingCountry': customerInfo.billing_country ,
                'billingCode': customerInfo.billing_code ,
                'billingPhone': customerInfo.billing_phone ,
                'billingFax': customerInfo.billing_fax ,
                'shippingAttention': customerInfo.shipping_attention ,
                'shippingAddressLine1': customerInfo.shipping_address_line_1 ,
                'shippingAddressLine2': customerInfo.shipping_address_line_2 ,
                'shippingCity': customerInfo.shipping_city ,
                'shippingState': customerInfo.shipping_state ,
                'shippingCountry': customerInfo.shipping_country ,
                'shippingCode': customerInfo.shipping_code,
                'shippingPhone': customerInfo.shipping_phone ,
                'shippingFax': customerInfo.shipping_fax ,
                'bankName': clientInfo.bank_name ,
                'bankAccountNumber': clientInfo.bank_account_number ,
                'ifsc': clientInfo.ifsc ,
                'accountType': clientInfo.account_type,

                # ----
                'brandName':  clientInfo.name,
                'brandPan':  clientInfo.pan,
                'brandGstin':  clientInfo.gst,
                'brandRegAddressLine1':  clientInfo.client_reg_address_line_1,
                'brandRegAddressLine2':  clientInfo.client_reg_address_line_2,
                'brandRegCity':  clientInfo.client_reg_city,
                'brandRegState':  clientInfo.client_reg_state,
                'brandRegCountry': clientInfo.client_reg_country,


                # 'itemTax': productInfo.intra_state_tax_name,
                # 'itemTaxType': productInfo.intra_state_tax_type,
                # 'itemTaxPercentage': productInfo.intra_state_tax_rate,
                
  


            }
           #print(invoiceInputDict)
            new_po_query = text(CREATE_INVOICE_INPUT)
            db.execute(new_po_query, invoiceInputDict)

            values = {'fulfilledQty': request.fulfilledQty, 'poLineItemId': request.poLineItemId}
            UPDATE_PURCHASE_ORDER_LINE_ITEM_FORMATTED = UPDATE_PURCHASE_ORDER_LINE_ITEM.format(**values)
            db.execute(text(UPDATE_PURCHASE_ORDER_LINE_ITEM_FORMATTED))
        
            values = {'poLineItemId': request.poLineItemId}
            UPDATE_PROCESSING_STATUS_FORMATTED = UPDATE_PROCESSING_STATUS.format(**values)
            db.execute(text(UPDATE_PROCESSING_STATUS_FORMATTED))
           
            values = { 'po_number': purchaseOrderNumber, 'fulfilledQty': request.fulfilledQty }
            UPDATE_PURCHASE_ORDER_DETAILS_FORMATTED = UPDATE_PURCHASE_ORDER_DETAILS.format(**values)
            db.execute(text(UPDATE_PURCHASE_ORDER_DETAILS_FORMATTED))
 

            values = {'customer_master_id':request.customerMasterId,'product_master_id':productInfo.id,'poLineItemId': request.poLineItemId }
            UPDATE_TAX_COLUMNS_FORMATTED = UPDATE_TAX_COLUMNS.format(**values)
            db.execute(text(UPDATE_TAX_COLUMNS_FORMATTED))

        db.commit()
        return {"message": "Invoice line item created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create invoice Order {request.poNumber}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create invoice Order {request.poNumber}: {str(e)}")

    
