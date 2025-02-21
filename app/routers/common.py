import os
import boto3
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Header, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.models import User
from dotenv import load_dotenv
from app.schemas import UploadPoSchema
from app.security import validate_token
from app.dependencies import get_db
from app.routers.utilities import convert_csv_to_json
from app.config.config import settings

# Initialize FastAPI router
load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

router = APIRouter()
security_scheme = HTTPBearer()

po_folder = settings.purchase_orders_folder
po_mapping = settings.po_mappings_folder
sample_po_folder = settings.sample_po
im_folder = settings.item_master_folder
im_mapping = settings.item_master_mappings_folder
cm_folder = settings.customer_master_folder
cm_mapping = settings.customer_master_mappings_folder

def ensure_s3_folders(client_name: str, page_id: str):
    if page_id == "po_page":
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{po_folder}/{sample_po_folder}/")
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{po_folder}/{po_mapping}/")
    elif page_id == "item_master_page":
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{im_folder}/")
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{im_folder}/{im_mapping}/")
    elif page_id == "customer_master_page":
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{cm_folder}/")
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{client_name}/{cm_folder}/{cm_mapping}/")
    else:
        raise HTTPException(status_code=400, detail="Invalid page_id for folder structure.")

def handle_po_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    file_extension = os.path.splitext(file.filename)[1]
    po_file_name = f"{client_name}-{sample_po_folder}{file_extension}"
    po_mappings_file_name = f"{client_name}-{po_mapping}.csv"

    ensure_s3_folders(client_name, page_id)

    file_path = f"{client_name}/{po_folder}/{sample_po_folder}/{po_file_name}"
    po_mappings_folder_path = f"{client_name}/{po_folder}/{po_mapping}/{po_mappings_file_name}"

    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to S3 failed: {str(e)}")

    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
    }

def handle_im_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    file_extension = os.path.splitext(file.filename)[1]
    im_file_name = f"{client_name}-{im_folder}{file_extension}"
    im_mappings_file_name = f"{client_name}-{im_mapping}.csv"

    ensure_s3_folders(client_name, page_id)

    file_path = f"{client_name}/{im_folder}/{im_file_name}"
    im_mappings_folder_path = f"{client_name}/{im_folder}/{im_mapping}/{im_mappings_file_name}"

    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to S3 failed: {str(e)}")

    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
    }

def handle_cm_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    file_extension = os.path.splitext(file.filename)[1]
    cm_file_name = f"{client_name}-{cm_folder}{file_extension}"
    cm_mappings_file_name = f"{client_name}-{cm_mapping}.csv"

    ensure_s3_folders(client_name, page_id)

    file_path = f"{client_name}/{cm_folder}/{cm_file_name}"
    cm_mappings_folder_path = f"{client_name}/{cm_folder}/{cm_mapping}/{cm_mappings_file_name}"

    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to S3 failed: {str(e)}")

    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
    }

@router.post("/upload/", response_model=UploadPoSchema)
def upload(
    db: Session = Depends(get_db),
    client_name: str = Query(..., description="Name of the client uploading the file"),
    file: UploadFile = File(...),
    current_user: User = Depends(security_scheme),
    page_id: str = Header(..., description="Page identifier for proper file handling"),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    try:
        if page_id == "po_page":
            return handle_po_file(db, file, client_name, hash, page_id)
        elif page_id == "item_master_page":
            return handle_im_file(db, file, client_name, hash, page_id)
        elif page_id == "customer_master_page":
            return handle_cm_file(db, file, client_name, hash, page_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid page_id.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
