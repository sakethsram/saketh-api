from fastapi import UploadFile
import os
import json
import shutil
import hashlib
import pandas as pd
from datetime import datetime
from app.config.config import settings

base_folder = settings.base_folder

def ensure_directory_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_sha256(file_path: str) -> str:
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def get_file_path(primary_folder: str, client_name: str, mappings_folder: str, file_name: str) -> str:
    """Generate a file path based on the folder structure."""
    today_date = datetime.now().strftime("%d-%m-%Y")
    folder_path = os.path.join(base_folder, primary_folder, client_name, mappings_folder, today_date)
    ensure_directory_exists(folder_path)
    return os.path.join(folder_path, file_name)

def save_file(file: UploadFile, file_path: str):
    """Save the uploaded file to the specified path."""
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def convert_xlsx_to_json(page_id):
    # Mapping between page IDs and corresponding file names
    page_to_file_mapping = {
        "po_page": "po-mapping.xlsx",
        "item_master_page": "itemmaster-mapping.xlsx",
        "customer_master_page": "custmaster-mapping.xlsx"
    }
    
    # Directory where the mappings are stored
    base_dir = "app/routers/data"

    # Check if the page_id exists in the mapping
    if page_id not in page_to_file_mapping:
        raise ValueError(f"Invalid page_id '{page_id}'. Supported pages are: {list(page_to_file_mapping.keys())}")
    
    # Construct the file path
    xlsx_file = os.path.join(base_dir, page_to_file_mapping[page_id])
    
    # Verify if the file exists
    if not os.path.exists(xlsx_file):
        raise FileNotFoundError(f"File '{xlsx_file}' does not exist.")
    
    # Read the Excel file and convert to JSON
    try:
        df = pd.read_excel(xlsx_file)
        df = df.fillna(value='-')
        json_data = df.to_dict(orient='records')
        return json_data
    except Exception as e:
        raise RuntimeError(f"Error processing file '{xlsx_file}': {str(e)}")

