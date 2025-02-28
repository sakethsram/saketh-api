import io
from datetime import date
from io import BytesIO
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Header
from fastapi import HTTPException
from fastapi import Query
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.helper.genericHelper import convertKeysToCamelCase
from app.models import EvenflowInvoicePayments
from app.utils.helpers import validate_authentication

router = APIRouter()
security_scheme = HTTPBearer()


@router.get("/settlementReports")
def list_invoice_payments(
    page: int = Query(1, ge=1, description="Page number",alias="page"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page",alias="pageSize"),
    invoice_number: Optional[str] = Query(None, description="Filter by invoice number",alias="invoiceNumber"),
    from_date: Optional[date] = Query(None, description="Filter by invoice date (from)",alias="fromDate"),
    to_date: Optional[date] = Query(None, description="Filter by invoice date (to)",alias="toDate"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    """Get a paginated list of invoice payments with optional filters."""
    validate_authentication(authorization=authorization, db=db)
    query = db.query(EvenflowInvoicePayments).filter(EvenflowInvoicePayments.active_flag == 1)
    if invoice_number:
        query = query.filter(EvenflowInvoicePayments.invoice_number == invoice_number)
    if from_date:
        query = query.filter(EvenflowInvoicePayments.invoice_date >= from_date)
    if to_date:
        query = query.filter(EvenflowInvoicePayments.invoice_date <= to_date)
    total_count = query.count()
    offset = (page - 1) * page_size
    results = query.order_by(EvenflowInvoicePayments.id.desc()).offset(offset).limit(page_size).all()
    payment_data = []
    for payment in results:
        payment_data.append({
            "id": payment.id,
            "clientId": payment.client_id,
            "evenflowCustomerMasterId": payment.evenflow_customer_master_id,
            "evenflowInvoiceId": payment.evenflow_invoice_id,
            "invoiceNumber": payment.invoice_number,
            "paymentNumber": payment.payment_number,
            "invoiceDate": payment.invoice_date,
            "transactionType": payment.transaction_type,
            "transactionDescription": payment.transaction_description,
            "referenceDetails": payment.reference_details,
            "originalInvoiceNumber": payment.original_invoice_number,
            "invoiceAmount": float(payment.invoice_amount),
            "invoiceCurrency": payment.invoice_currency,
            "withholdingAmount": float(payment.withholding_amount),
            "termsDiscountTaken": float(payment.terms_discount_taken),
            "amountPaid": float(payment.amount_paid),
            "remainingAmount": float(payment.remaining_amount),
            "createdOn": payment.created_on.isoformat(),
            "createdBy": payment.created_by,
            "modifiedOn": payment.modified_on.isoformat(),
            "modifiedBy": payment.modified_by,
            "activeFlag": payment.active_flag
        })
    return {
        "total": total_count,
        "page": page,
        "pageSize": page_size,
        "data": payment_data
    }

@router.get("/settlementReports/export")
def export_invoice_payments_to_excel(
    invoice_number: Optional[str] = Query(None, description="Filter by invoice number"),
    payment_number: Optional[str] = Query(None, description="Filter by payment number"),
    from_date: Optional[date] = Query(None, description="Filter by invoice date (from)"),
    to_date: Optional[date] = Query(None, description="Filter by invoice date (to)"),
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    """Export invoice payments data to Excel with optional filters."""
    validate_authentication(authorization=authorization, db=db)
    query = db.query(EvenflowInvoicePayments).filter(EvenflowInvoicePayments.active_flag == 1)
    if invoice_number:
        query = query.filter(EvenflowInvoicePayments.invoice_number == invoice_number)
    if payment_number:
        query = query.filter(EvenflowInvoicePayments.payment_number == payment_number)
    if from_date:
        query = query.filter(EvenflowInvoicePayments.invoice_date >= from_date)
    if to_date:
        query = query.filter(EvenflowInvoicePayments.invoice_date <= to_date)
    results = query.order_by(EvenflowInvoicePayments.id.desc()).all()
    if not results:
        raise HTTPException(status_code=404, detail="No data found with the specified filters")
    data = []
    for payment in results:
        data.append({
            "ID": payment.id,
            "Client ID": payment.client_id,
            "Customer ID": payment.evenflow_customer_master_id,
            "Invoice ID": payment.evenflow_invoice_id,
            "Invoice Number": payment.invoice_number,
            "Payment Number": payment.payment_number,
            "Invoice Date": payment.invoice_date,
            "Transaction Type": payment.transaction_type,
            "Transaction Description": payment.transaction_description,
            "Reference Details": payment.reference_details,
            "Original Invoice Number": payment.original_invoice_number,
            "Invoice Amount": float(payment.invoice_amount),
            "Currency": payment.invoice_currency,
            "Withholding Amount": float(payment.withholding_amount),
            "Discount Taken": float(payment.terms_discount_taken),
            "Amount Paid": float(payment.amount_paid),
            "Remaining Amount": float(payment.remaining_amount),
            "Created On": payment.created_on,
            "Created By": payment.created_by,
            "Modified On": payment.modified_on,
            "Modified By": payment.modified_by
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Invoice Payments', index=False)
        worksheet = writer.sheets['Invoice Payments']
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col) + 2)
            worksheet.set_column(i, i, column_width)
    output.seek(0)
    from datetime import datetime
    filename = f"invoice_payments_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/uploadPayments")
async def upload_payments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents), header=None)

        expected_columns = {
            "Invoice Number", "Payment Number", "Invoice Date", "Transaction type",
            "Transaction Description", "Reference Details", "Original Invoice Number",
            "Invoice Amount", "Invoice Currency", "Withholding Amount",
            "Terms Discount Taken", "Amount Paid", "Remaining Amount",
        }
        header_row_index = None
        for index, row in df.iterrows():
            if expected_columns.issubset(set(row.astype(str))):
                header_row_index = index
                break
        if header_row_index is None:
            raise HTTPException(status_code=400, detail="Could not find header row in the Excel file.")
        df = pd.read_excel(BytesIO(contents), header=header_row_index)
        if not expected_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400, 
                detail=f"Missing columns: {expected_columns - set(df.columns)}"
            )
        records = []
        for _, row in df.iterrows():
            record = EvenflowInvoicePayments(
                client_id=1,
                evenflow_customer_master_id=0,
                evenflow_invoice_id=0,
                invoice_number=row["Invoice Number"],
                payment_number=row["Payment Number"],
                invoice_date=row["Invoice Date"],
                transaction_type=row["Transaction type"],
                transaction_description=row.get("Transaction Description"),
                reference_details=row["Reference Details"],
                original_invoice_number=row.get("Original Invoice Number"),
                invoice_amount=row["Invoice Amount"],
                invoice_currency=row["Invoice Currency"],
                withholding_amount=row.get("Withholding Amount", 0),
                terms_discount_taken=row.get("Terms Discount Taken", 0),
                amount_paid=row.get("Amount Paid", 0),
                remaining_amount=row.get("Remaining Amount", 0),
                created_by=row.get("Created By"),
                modified_by=row.get("Modified By"),
                active_flag=1
            )
            records.append(record)
            db.add_all(records)
            db.commit()
        return {"message": "Data inserted successfully", "rows_inserted": len(records)}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

