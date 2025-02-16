from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models import EvenflowInvoiceInputs
from app.models import EvenflowInvoices
from app.models import EvenflowInvoicesLineItems
from app.models import EvenflowPurchaseOrder
from app.models import EvenflowPurchaseOrderLineItem
from app.schemas import InvoiceInputRecord
from app.schemas import InvoiceInputResponse
from app.utils.enums import InvoiceStatusEnum
from app.utils.enums import POLineItemProcessingStatusEnum
from app.utils.enums import POProcessingStatusEnum


def get_invoice_inputs(db: Session, invoice_inputs_id: int)-> EvenflowInvoiceInputs:
    return (
        db.query(EvenflowInvoiceInputs).filter(EvenflowInvoiceInputs.id == invoice_inputs_id).first()
    )
def get_in_progress_po_numbers(db: Session) -> list[EvenflowPurchaseOrder]:
    return (
        db.query(EvenflowPurchaseOrder).filter(
            EvenflowPurchaseOrder.po_processing_status.in_(
                [
                    POProcessingStatusEnum.IN_PROGRESS_PARTIAL.value,
                    POProcessingStatusEnum.IN_PROGRESS_FULL.value,
                ]
            )
        )
    ).all()

def get_invoice_by_id(db: Session, invoice_obj:EvenflowInvoiceInputs,invoice_id: int):
    return db.query(EvenflowInvoiceInputs).filter(EvenflowInvoiceInputs.id == invoice_obj.id).first()

def get_invoices_by_po(db: Session, po_number: str):
    return db.query(EvenflowInvoiceInputs).filter(EvenflowInvoiceInputs.purchase_order_number == po_number).all()


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
        EvenflowInvoiceInputs.invoice_date
    ).filter(EvenflowInvoiceInputs.purchase_order_number == po_number,
             EvenflowInvoiceInputs.invoice_status==InvoiceStatusEnum.NOT_RAISED.value,
             EvenflowPurchaseOrderLineItem.po_line_item_processing_status in (
                 POLineItemProcessingStatusEnum.OPEN.value,
                 POLineItemProcessingStatusEnum.PARTIALLY_FULFILLED.value)).join(EvenflowPurchaseOrderLineItem, 
           EvenflowInvoiceInputs.evenflow_purchase_orders_line_items_id == EvenflowPurchaseOrderLineItem.id)
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
            invoiceInputs=f"http://localhost:8000/exportInvoiceInputsData/{po_number}?invoiceInputsId={r[0]}",
        )
        for r in results
    ]
    return InvoiceInputResponse(
        invoiceInputsRecordCount={"totalrecords": total_records},
        invoiceInputsRecords=records,
    )



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
    db.commit()
    return invoice_obj



def get_invoices_by_invoice_number(db: Session, invoice_number: str):
    return db.query(EvenflowInvoiceInputs).filter(EvenflowInvoiceInputs.invoice_number == invoice_number).all()


def create_invoice(db: Session, invoice_data: dict):
    """Create a new invoice from a dictionary input."""
    invoice = EvenflowInvoices(**invoice_data)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def create_invoice_line_items(db: Session, line_items_data: list, invoice_id: int):
    """Create new invoice line items linked to an invoice."""
    line_items = [EvenflowInvoicesLineItems(**item) for item in line_items_data]
    db.add_all(line_items)
    db.commit()
    return line_items



def update_po_processing_status(db: Session, po_number: str):
    """Updates the PO processing status based on fulfillment status of its line items."""

    purchase_order_obj=db.query(EvenflowPurchaseOrder).filter(EvenflowPurchaseOrder.po_number==po_number).first()
    po_line_items = db.query(EvenflowPurchaseOrderLineItem).filter(EvenflowPurchaseOrderLineItem.evenflow_purchase_orders_id==purchase_order_obj.id).all()

    for line_item in po_line_items:
        sq1 = line_item.qty_requested
        fq1 = db.query(func.sum(EvenflowInvoiceInputs.accepted_qty)).filter(EvenflowInvoiceInputs.evenflow_purchase_orders_line_items_id==line_item.id).scalar() or 0

        if sq1 == 0:
            status = 'OPEN'
        elif sq1 > fq1:
            status = 'PARTIALLY_FULFILLED'
        else:
            status = 'FULFILLED'

        line_item.po_line_item_processing_status = status
        db.query(EvenflowInvoiceInputs).filter_by(evenflow_purchase_orders_line_items_id=line_item.id).update({"po_line_item_processing_status": status})

    db.commit()

    if db.query(EvenflowPurchaseOrderLineItem).filter(
        EvenflowPurchaseOrderLineItem.purchase_order_number == po_number,
        EvenflowPurchaseOrderLineItem.po_line_item_processing_status.in_(['OPEN', 'PARTIALLY_FULFILLED'])
    ).count() > 0:
        po_status = 'PARTIALLY_FULFILLED'
    else:
        po_status = 'FULFILLED'

    db.query(EvenflowPurchaseOrder).filter_by(purchase_order_number=po_number).update({"po_processing_status": po_status})
    db.commit()