"""Invoice Generation Routes."""
from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.cruds.get_invoice_inputs_po_numbers_cruds import get_in_progress_po_numbers
from app.cruds.get_invoice_inputs_po_numbers_cruds import get_invoice_by_id
from app.cruds.get_invoice_inputs_po_numbers_cruds import get_invoice_inputs_with_po_number
from app.cruds.get_invoice_inputs_po_numbers_cruds import get_invoices_by_invoice_number
from app.cruds.get_invoice_inputs_po_numbers_cruds import get_invoices_by_po
from app.cruds.get_invoice_inputs_po_numbers_cruds import update_invoice_input
from app.cruds.get_invoice_inputs_po_numbers_cruds import update_po_processing_status
from app.dependencies import get_db
from app.helper.genericHelper import convertKeysToCamelCase
from app.models import EvenflowInvoices
from app.schemas import GenerateInvoiceRequest
from app.schemas import InvoiceInputResponse
from app.schemas import InvoiceInputsUpdateRequest
from app.schemas import InvoiceInputsUpdateResponse
from app.utils.enums import InvoiceStatusEnum
from app.utils.helpers import get_invoice_json
from app.utils.helpers import process_invoice_from_inputs
from app.utils.helpers import read_pdf_as_bytes
from app.utils.helpers import upload_pdf_to_s3
from app.utils.helpers import validate_authentication
from app.utils.logger import logger

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/listPOForInvoice", response_model=dict)
def list_po_for_invoice(
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
)-> JSONResponse:
    validate_authentication(authorization=authorization,db=db)

    try:
        po_records_obj = get_in_progress_po_numbers(db)
        po_records_list = [
            {"purchaseOrderId": po_record.id, "poNumber": po_record.po_number}
            for po_record in po_records_obj
        ]
        return JSONResponse(
            {
                "poRecordCount": {"totalrecords": len(po_records_obj)},
                "poRecords": po_records_list,
            }
        )
    except Exception as e:
        logger.error(f"Failed to listPOForInvoice: {e}")
        raise HTTPException(
            status_code=500, detail=f"Fetching from Database Failed: {e!s}"
        )


@router.get("/listInvoiceInputs/{poNumber}", response_model=InvoiceInputResponse)
def list_invoice_inputs(
    po_number:str = Path(..., alias="poNumber"),
    page_size: int = Query(10, alias="pageSize"),
    page_number: int = Query(1, alias="pageNumber"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
)->InvoiceInputResponse:
    validate_authentication(authorization=authorization,db=db)
    return get_invoice_inputs_with_po_number(db, po_number, page_size, page_number)


@router.get("/exportInvoiceInputs", response_class=StreamingResponse)
def export_invoice_inputs_data(
    po_number: Optional[str] = Query(None, alias="poNumber"),
    invoice_inputs_id: Optional[int] = Query(None, alias="invoiceInputsId"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
) -> StreamingResponse:
    """
    Export invoice data based on either PO number or invoice input ID.
    Returns an Excel file containing the invoice data.
    """
    try:
        validate_authentication(authorization=authorization, db=db)
        if not po_number and not invoice_inputs_id:
            raise HTTPException(
                status_code=400, 
                detail="Either poNumber or invoiceInputsId must be provided"
            )
        
        list_of_invoices_inputs = []
        filename_suffix = ""
        
        if po_number:
            invoices = get_invoices_by_po(db, po_number)
            if not invoices:
                raise HTTPException(
                    status_code=404, 
                    detail="No invoices found for the given PO number"
                )
            filename_suffix = f"po_{po_number}"
    
            for invoice in invoices:
                invoice_dict = convertKeysToCamelCase(invoice.to_dict())
                data = OrderedDict(
                        (key, [value]) 
                        for key, value in invoice_dict.items() 
                        if key != "SaInstanceState"
                    )
                list_of_invoices_inputs.append(data)
        
        elif invoice_inputs_id:
            invoice = get_invoice_by_id(db, invoice_inputs_id)
            if not invoice:
                raise HTTPException(
                    status_code=404, 
                    detail="Invoice not found for the given ID"
                )
            filename_suffix = f"invoice_{invoice_inputs_id}"
            
            invoice_dict = convertKeysToCamelCase(invoice.to_dict())
            data = OrderedDict(
                        (key, [value]) 
                        for key, value in invoice_dict.items() 
                        if key != "SaInstanceState"
                    )
            list_of_invoices_inputs.append(data)
        
        df = pd.concat([pd.DataFrame(data) for data in list_of_invoices_inputs])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="InvoiceInputsData")
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=invoice_inputs_{filename_suffix}.xlsx"
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(e)}
        )

@router.patch("/updateInvoiceInputs", response_model=InvoiceInputsUpdateResponse)
def update_invoice_inputs(
    request: InvoiceInputsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
)-> InvoiceInputsUpdateResponse:
    try:
        validate_authentication(authorization=authorization,db=db)
        updated_records = []
        for update in request.updates:
            update_data = update.model_dump(exclude_unset=True)
            updated_invoices_input_obj = update_invoice_input(
                db=db, invoice_inputs_id=update_data["id"], update_data=update_data
            )
            updated_records.append(updated_invoices_input_obj.to_dict())
        return InvoiceInputsUpdateResponse(
            message="Invoice inputs updated successfully for Preview",
            updatedRecords=convertKeysToCamelCase(updated_records),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(e)}
        )

@router.post("/generateInvoice", status_code=201)
def generate_invoice(
    request: GenerateInvoiceRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
)-> JSONResponse:
    validate_authentication(authorization=authorization,db=db)
    invoice_number = request.invoiceNumber
    if(db.query(EvenflowInvoices).filter(EvenflowInvoices.invoice_number == invoice_number).all()):
        raise HTTPException(status_code=400,detail=f"Invoice already generated with Invoice number {invoice_number}")
    invoice_obj=get_invoices_by_invoice_number(db=db,invoice_number=invoice_number)
    response=get_invoice_json(invoices=invoice_obj)

    #### UNCOMMENT THIS WHILE DEPLOYING
    # status,invoice_number,pdf_content = create_invoice(po_data=response.get("po_data"),customer_data=response.get("customer_data"),item_data=response.get("item_data"),x_invoice_number=invoice_number)


    status, invoice_number,pdf_content = 'success',f'{invoice_number}',read_pdf_as_bytes(file_path='sample_invoice.pdf')
    if status == 'error':
        raise HTTPException(status_code=400, detail="something went wrong, please try again later")
    upload_path=upload_pdf_to_s3(file=pdf_content,po_number=response.get('po_data').get('po_number'),invoice_number=invoice_number)
    invoice=process_invoice_from_inputs(db=db,invoice_inputs=invoice_obj,s3_uploaded_path=upload_path)
    for invoice_input_item in invoice_obj:
        invoice_input_item.invoice_status = InvoiceStatusEnum.RAISED.value
    db.commit()

    update_po_processing_status(db=db,po_number=invoice_obj[0].purchase_order_number)
    
    return {
        "message": "Invoice generated successfully.",
        "invoiceDetails": {
            "invoiceId": invoice.id,
            "clientId": invoice.client_id,
            "evenflowCustomerMasterId": invoice.evenflow_customer_master_id,
            "evenflowProductMasterId": invoice.evenflow_product_master_id,
            "invoiceNumber": invoice.invoice_number,
            "estimateNumber": invoice.estimate_number,
            "invoiceDate": invoice.invoice_date,
            "invoiceAmount": float(invoice.invoice_amount),
            "invoiceStatus": invoice.invoice_status,
            "customerName": invoice.customer_name,
            "paymentDueDate": (invoice.invoice_date + datetime.timedelta(days=45)),
            "paymentTerms": "Next due in 45 days",
            "poFilePath": invoice.po_file_path,
            "invoiceInputsFilePath": invoice.invoice_inputs_file_path,
            "invoiceFilePath": invoice.invoice_file_path,
            "createdOn": invoice.created_on.isoformat(),
            "createdBy": invoice.created_by,
            "modifiedOn": invoice.modified_on.isoformat(),
            "modifiedBy": invoice.modified_by,
        },
    }