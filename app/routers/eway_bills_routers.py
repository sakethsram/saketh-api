"""Invoice Generation Routes."""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import EvenflowInvoices
from app.models import EvenflowInvoicesEwayBills
from app.schemas import EwayBillUpdateRequest
from app.schemas import GenerateEwayBillRequest
from app.utils.helpers import read_pdf_as_bytes
from app.utils.helpers import upload_pdf_to_s3
from app.utils.helpers import validate_authentication
from app.utils.logger import logger

router = APIRouter()
security_scheme = HTTPBearer()


@router.get("/listInvoicesForEwayBills", response_model=dict)
def list_invoices_for_eway_bills(
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
) -> JSONResponse:
    validate_authentication(authorization=authorization, db=db)

    try:
        invoices_obj = db.query(EvenflowInvoices).filter(EvenflowInvoices.invoice_amount > 50000).all()
        invoices_list = [
            {"invoiceId": invoice.id, "invoiceNumber": invoice.invoice_number}
            for invoice in invoices_obj
        ]
        return JSONResponse(
            {
                "invoiceRecordCount": {"totalrecords": len(invoices_obj)},
                "invoiceRecords": invoices_list,
            }
        )
    except Exception as e:
        logger.error(f"Failed to listInvoicesForEwayBills: {e}")
        raise HTTPException(
            status_code=500, detail=f"Fetching from Database Failed: {e!s}"
        ) from None



@router.get("/listInvoicesDetailsForEwayBills/{invoiceNumber}", response_model=dict)
def invoices_for_eway_bills(
    invoice_number:str = Path(..., alias="invoiceNumber"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
) -> JSONResponse:
    validate_authentication(authorization=authorization, db=db)

    try:
        invoices_obj = db.query(EvenflowInvoices).filter(EvenflowInvoices.invoice_number == invoice_number).all()
        invoices_list = [
            {   "invoiceId":invoice.id,
                "purchaseOrderNumber": invoice.purchase_order_number,
                "invoiceNumber": invoice.invoice_number,
                "ewayBillNumber": "",
                "transportProviderName": "",
                "transportProviderContact": "",
                "transportProviderVehicleNumber": "",
                "notes": invoice.notes,
            }
            for invoice in invoices_obj
        ]
        return JSONResponse(
            {
                "invoiceRecordCount": {"totalrecords": len(invoices_obj)},
                "invoiceRecords": invoices_list,
            }
        )
    except Exception as e:
        logger.error(f"Failed to listInvoicesForEwayBills: {e}")
        raise HTTPException(
            status_code=500, detail=f"Fetching from Database Failed: {e!s}"
        ) from None



@router.put("/updateEwayBill", response_model=dict)
def update_eway_bill(
    request: EwayBillUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
) -> JSONResponse:
    validate_authentication(authorization=authorization, db=db)
    try:
        invoice_record = db.query(EvenflowInvoices).filter(
            EvenflowInvoices.invoice_number == request.invoiceNumber
        ).first()
        if not invoice_record:
            raise HTTPException(status_code=404, detail="Invoice not found")
        eway_bill_record= EvenflowInvoicesEwayBills()
        eway_bill_record.eway_bill_number = request.ewayBillNumber
        eway_bill_record.transport_provider_company_name = request.transportProviderName
        eway_bill_record.transport_provider_contact_name = request.transportProviderContact
        eway_bill_record.transport_provider_contact_number = request.transportProviderContact
        eway_bill_record.transport_provider_vehicle_number = request.transportProviderVehicleNumber
        eway_bill_record.notes = request.notes if request.notes is not None else ""
        eway_bill_record.evenflow_invoices_id = request.id
        eway_bill_record.purchase_order_number = invoice_record.purchase_order_number
        eway_bill_record.invoice_number = invoice_record.invoice_number
        db.add(eway_bill_record)
        db.commit()
        db.refresh(eway_bill_record)
        return JSONResponse(
            {
                "message": "Eway bill details updated successfully for Preview.",
                "updatedRecord": {
                    "invoiceNumber": eway_bill_record.invoice_number,
                    "ewayBillNumber": eway_bill_record.eway_bill_number,
                    "transportProviderName": eway_bill_record.transport_provider_company_name,
                    "transportProviderContact": eway_bill_record.transport_provider_contact_name,
                    "transportProviderVehicleNumber": eway_bill_record.transport_provider_vehicle_number,
                    "notes": eway_bill_record.notes,
                    "gstNumber": invoice_record.gstin
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating Eway Bill details: {str(e)}"
        ) from None


@router.post("/generateEwayBill", status_code=201)
def generate_eway_bill(
    request: GenerateEwayBillRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
) -> JSONResponse:
    validate_authentication(authorization=authorization, db=db)
    eway_bill_number = request.ewayBillNumber
    eway_bill_obj = db.query(EvenflowInvoicesEwayBills).filter(
        EvenflowInvoicesEwayBills.eway_bill_number == eway_bill_number
    ).first()
    if not eway_bill_obj:
        raise HTTPException(status_code=404, detail=f"Invoice not found with Invoice number {eway_bill_number}")
    #### UNCOMMENT THIS WHILE DEPLOYING
    # status, eway_bill_number, pdf_content = create_eway_bill(invoice_number=invoice_number)
    # Mocked response for development
    status, eway_bill_number, pdf_content = 'success', f'EWB{eway_bill_number}', read_pdf_as_bytes(file_path='sample_eway_bill.pdf')
    if status == 'error':
        raise HTTPException(status_code=400, detail="Something went wrong generating eWay bill, please try again later")
    upload_path = upload_pdf_to_s3(
        file=pdf_content,
        po_number=eway_bill_obj.purchase_order_number,
        invoice_number="invoice_number",
        document_type="eway_bill"
    )
    eway_bill_obj.active_flag=True
    db.commit()
    db.refresh(eway_bill_obj)
    return {
        "message": "eWay bill generated successfully.",
        "ewayBillDetails": {
            "ewayBillId": eway_bill_obj.id,
            "invoiceId": eway_bill_obj.id,
            "invoiceNumber": eway_bill_obj.invoice_number,
            "ewayBillNumber": eway_bill_obj.eway_bill_number,
            "ewayBillStatus": eway_bill_obj.eway_bill_status,
            "ewayBillFilePath": eway_bill_obj.eway_bill_file_path,
            "createdOn": eway_bill_obj.created_on.isoformat(),
            "createdBy": eway_bill_obj.created_by,
            "modifiedOn": eway_bill_obj.modified_on.isoformat(),
            "modifiedBy": eway_bill_obj.modified_by,
        }
    } # type: ignore

