from sqlalchemy.orm import Session

from app.models import EvenflowInvoiceInputs, EvenflowPurchaseOrder
from app.schemas import InvoiceInputRecord, InvoiceInputResponse
from app.utils.utilities import POProcessingStatusEnum



def get_invoice_inputs(db: Session, invoice_inputs_id: int):
    invoice_obj = (
        db.query(EvenflowInvoiceInputs).filter(EvenflowInvoiceInputs.id == invoice_inputs_id).first()
    )
    return invoice_obj
def get_in_progress_po_numbers(db: Session) -> list[EvenflowPurchaseOrder]:
    po_obj = (
        db.query(EvenflowPurchaseOrder).filter(
            EvenflowPurchaseOrder.po_processing_status.in_(
                [
                    POProcessingStatusEnum.IN_PROGRESS_PARTIAL.value,
                    POProcessingStatusEnum.IN_PROGRESS_FULL.value,
                ]
            )
        )
    ).all()
    return po_obj


def get_po_number(po_number: str, db: Session) -> EvenflowPurchaseOrder:
    po_obj = (
        db.query(EvenflowPurchaseOrder)
        .filter(EvenflowPurchaseOrder.po_number == po_number)
        .one()
    )
    return po_obj


def get_invoice_inputs_with_po_number(
    db: Session, po_number: str, page_size: int, page_number: int
) -> InvoiceInputResponse:
    query = db.query(
        EvenflowInvoiceInputs.id,
        EvenflowInvoiceInputs.invoice_number,
        EvenflowInvoiceInputs.customer_name,
        EvenflowInvoiceInputs.item_price,
        EvenflowInvoiceInputs.expected_payment_date,
        EvenflowInvoiceInputs.payment_terms,
        EvenflowInvoiceInputs.po_file_path,
        EvenflowInvoiceInputs.quantity,
    ).filter(EvenflowInvoiceInputs.purchase_order_number == po_number)
    total_records = query.count()
    results = query.offset((page_number - 1) * page_size).limit(page_size).all()

    records = [
        InvoiceInputRecord(
            invoiceInputsId=r[0],
            invoiceNumber=r[1],
            customerName=r[2],
            invoiceAmount=r[3] * r[7],
            paymentDueDate=r[4],
            paymentTerms=f"Due in {r[5]} Days",
            poFilePath=r[6],
            invoiceInputs=f"http://localhost:8000/exportInvoiceInputsData/{r[0]}",
        )
        for r in results
    ]

    return InvoiceInputResponse(
        invoiceInputsRecordCount={"totalrecords": total_records},
        invoiceInputsRecords=records,
    )


from fastapi.exceptions import HTTPException
def update_invoice_input(db: Session, invoice_inputs_id: int, update_data: dict):
    invoice_obj = get_invoice_inputs(db=db, invoice_inputs_id=invoice_inputs_id)
    if not invoice_obj:
        raise HTTPException(
            status_code=404, detail=f"Invoice input with ID {update_data.id} not found"
        )
    from datetime import datetime

    for field, value in update_data.items():
        if hasattr(invoice_obj, field):
            setattr(invoice_obj, field, value)
    invoice_obj.modified_on = datetime.now()
    return invoice_obj