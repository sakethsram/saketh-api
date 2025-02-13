from datetime import datetime
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.cruds.get_invoice_inputs_po_numbers_cruds import (
    get_in_progress_po_numbers,
    get_invoice_inputs_with_po_number,
    update_invoice_input,
)
from app.dependencies import get_db
from app.helper.genericHelper import convertKeysToCamelCase
from app.models import (
    EvenflowInvoiceInputs,
)
from app.schemas import (
    GenerateInvoiceRequest,
    InvoiceInputResponse,
    InvoiceInputsUpdateRequest,
    InvoiceInputsUpdateResponse,
)
from app.security import validate_token
from app.utils.logger import logger

router = APIRouter()
security_scheme = HTTPBearer()


@router.get("/listPOForInvoice", response_model=dict)
def list_po_for_invoice(
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=403, detail="Invalid Authorization header format"
        )

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(
            f"Request received for /listPOForInvoice from - {payload.get('user_login_id')}"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

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
            status_code=500, detail=f"Fetching from Database Failed: {str(e)}"
        )


@router.get("/listInvoiceInputs/{poNumber}", response_model=InvoiceInputResponse)
def list_invoice_inputs(
    poNumber: str,
    pageSize: int = Query(10, alias="pageSize"),
    pageNumber: int = Query(1, alias="pageNumber"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=403, detail="Invalid Authorization header format"
        )

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        logger.info(
            f"Request received for /listInvoiceInputs/{poNumber} from - {payload.get('user_login_id')}"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    return get_invoice_inputs_with_po_number(db, poNumber, pageSize, pageNumber)


@router.get(
    "/exportInvoiceInputsData/{invoiceInputsId}", response_class=StreamingResponse
)
def export_invoice_inputs_data(
    invoiceInputsId: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    invoice_obj = (
        db.query(EvenflowInvoiceInputs)
        .filter(EvenflowInvoiceInputs.id == invoiceInputsId)
        .first()
    )
    invoice_dict = convertKeysToCamelCase(invoice_obj.__dict__) if invoice_obj else None
    if not invoice_obj:
        raise HTTPException(status_code=404, detail="Invoice input not found")
    data = {
        key: [value]
        for key, value in invoice_dict.items()
        if key != "_sa_instance_state"
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="InvoiceInputsData")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=invoice_{invoiceInputsId}.xlsx"
        },
    )


@router.patch("/updateInvoiceInputs", response_model=InvoiceInputsUpdateResponse)
def update_invoice_inputs(
    request: InvoiceInputsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    updated_records = []
    for update in request.updates:
        update_data = update.model_dump(exclude_unset=True)
        updated_invoices_input_obj = update_invoice_input(
            db=db, invoice_inputs_id=update_data["id"], update_data=update_data
        )
        updated_records.append(updated_invoices_input_obj.to_dict())
    return InvoiceInputsUpdateResponse(
        message="Invoice inputs updated successfully for Preview",
        updatedRecords=updated_records,
    )


@router.post("/generateInvoice", status_code=201)
def generate_invoice(
    request: GenerateInvoiceRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    invoice_number = request.invoiceNumber

    invoice = (
        db.query(EvenflowInvoiceInputs).filter_by(invoice_number=invoice_number).first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    #logic to be changed.
    response = {
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
    return response
