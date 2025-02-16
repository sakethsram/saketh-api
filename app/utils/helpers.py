import os
from datetime import datetime
from io import BytesIO
from typing import Optional

import boto3
from fastapi import Header
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.cruds.get_invoice_inputs_po_numbers_cruds import create_invoice
from app.cruds.get_invoice_inputs_po_numbers_cruds import create_invoice_line_items
from app.models import EvenflowInvoices
from app.models import EvenflowInvoicesLineItems
from app.security import validate_token
from app.utils.logger import logger


def save_pdf(file_name: str, pdf_content: bytes, save_dir: str = "invoices") -> str:
    """Saves the given PDF content to a specified folder with a .pdf extension.

    :param file_name: Name of the PDF file to be saved (without extension or with .pdf)
    :param pdf_content: Byte content of the PDF file
    :param save_dir: Directory where the file should be saved (default: 'invoices')
    :return: Full file path of the saved PDF
    """
    os.makedirs(save_dir, exist_ok=True)
    if not file_name.lower().endswith(".pdf"):
        file_name += ".pdf"
    file_path = os.path.join(save_dir, file_name)
    with open(file_path, "wb") as file:
        file.write(pdf_content)
    return file_path

def read_pdf_as_bytes(file_path: str) -> bytes:
    """Reads a PDF file and returns its content in byte format.

    :param file_path: Path to the PDF file
    :return: Byte content of the PDF file
    """
    with open(file_path, "rb") as file:
        return file.read()

def upload_pdf_to_s3(file: bytes, po_number: str, invoice_number: str) -> Optional[str]:
    """Uploads a PDF file to an S3 bucket under a structured folder path.

    :param file: Byte content of the PDF file
    :param po_number: The purchase order number used in the folder structure
    :param invoice_number: The invoice number used as the file name
    :return: S3 file URL if successful, otherwise None
    """
    FOLDER_PATH = os.getenv("UPLOAD_FOLDER", "uploads")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    os.makedirs(FOLDER_PATH, exist_ok=True)
    file_name = f"{invoice_number}.pdf"
    file_path = os.path.join(FOLDER_PATH, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file)

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    s3 = session.client("s3")

    current_date = datetime.now().strftime("%Y-%m-%d")
    s3_key = f"evenflow/purchase-orders/{current_date}/{po_number}/{file_name}"

    try:
        s3.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=s3_key,
            Body=BytesIO(file),
            ContentType="application/pdf"
        )
        return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"  # noqa: TRY300
    except Exception as e:
        logger.error(f"Error uploading file to S3: {str(e)}")
        return None

def process_invoice_from_inputs(db: Session, 
                                invoice_inputs: list[EvenflowInvoicesLineItems], 
                                s3_uploaded_path: str) -> Optional[EvenflowInvoices]:
    """Processes invoice inputs, creates an invoice and its associated line items.

    :param db: Database session
    :param invoice_inputs: List of invoice input objects
    :param s3_uploaded_path: S3 URL of the uploaded invoice file
    :return: Created EvenflowInvoices object or None if inputs are empty
    """
    if not invoice_inputs:
        return None

    common_keys = set(EvenflowInvoices.__table__.columns.keys())
    invoice_data = {key: getattr(invoice_inputs[0], key, None) for key in common_keys}
    invoice_data["invoice_amount"] = sum(inp.item_price * inp.quantity for inp in invoice_inputs)
    invoice_data["active_flag"] = 1
    invoice_data["invoice_file_path"] = s3_uploaded_path
    invoice_data.pop("id", None)

    invoice = create_invoice(db, invoice_data)

    line_item_keys = set(EvenflowInvoicesLineItems.__table__.columns.keys())
    line_items_data = [
        {key: getattr(inp, key) for key in line_item_keys if hasattr(inp, key)} | {
            "evenflow_invoice_inputs_id": inp.id,
            "evenflow_invoices_id": invoice.id,
            "active_flag": 1,
        }
        for inp in invoice_inputs
    ]

    create_invoice_line_items(db, line_items_data, invoice.id)
    return invoice
def get_invoice_json(invoices):
    first_invoice = invoices[0]
    return {
        "po_data": {
            "place_of_supply": first_invoice.place_of_supply,
            "po_number": first_invoice.purchase_order_number,
            "total_box_count": first_invoice.total_box_count or 0,
            "po_line_items": [
                {
                    "qty_requested": invoice.quantity,
                    "unit_cost": invoice.item_price
                } for invoice in invoices
            ]
        },
        "customer_data": {
            "contact_id": str(first_invoice.evenflow_customer_master_id),
            "gst_treatment": first_invoice.gst_treatment,
            "gst_identification_number": first_invoice.gstin,
            "payment_terms": first_invoice.payment_terms,
            "payment_terms_label": first_invoice.payment_terms_label
        },
        "item_data": {
            "item_id": first_invoice.evenflow_product_master_id,
            "hsn_sac": first_invoice.hsn_sac,
            "usage_unit": first_invoice.usage_unit
        },
        "x_invoice_number": first_invoice.invoice_number or "AUTO-GENERATED"
    }
def validate_authentication(authorization: str = Header(...), db: Session = None) -> None:
    """Validates the authentication token from the Authorization header.

    :param authorization: Authorization header value
    :param db: Database session
    :raises HTTPException: If authentication fails
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    try:
        logger.info(f"Request received - {payload.get('user_login_id')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e!s}")  # noqa: B904




