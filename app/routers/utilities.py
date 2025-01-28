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

def get_file_path(client_name: str, primary_folder: str, subfolder: str, file_name: str) -> str:
    """
    Generate a file path based on the client name, folder type, and file name.
    This is used for primary files (e.g., sample PO, Item Master, Customer Master).
    """
    folder_path = os.path.join(base_folder, client_name, primary_folder, subfolder)
    ensure_directory_exists(folder_path)
    return os.path.join(folder_path, file_name)

def save_file(file: UploadFile, file_path: str):
    """Save the uploaded file to the specified path."""
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def convert_csv_to_json(page_id):
    # Mapping between page IDs and corresponding file names
    page_to_file_mapping = {
        "po_page": "evenflow-po-mappings.csv",
        "item_master_page": "evenflow-item-master-mappings.csv",
        "customer_master_page": "evenflow-customer-master-mappings.csv"
    }
    
    # Directory where the mappings are stored
    base_dir = "app/routers/data"

    # Check if the page_id exists in the mapping
    if page_id not in page_to_file_mapping:
        raise ValueError(f"Invalid page_id '{page_id}'. Supported pages are: {list(page_to_file_mapping.keys())}")
    
    # Construct the file path
    csv_file = os.path.join(base_dir, page_to_file_mapping[page_id])
    
    # Verify if the file exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File '{csv_file}' does not exist.")
    
    # Read the CSV file and convert to JSON
    try:
        df = pd.read_csv(csv_file)
        df = df.fillna(value='')  # Replace NaN values with '-' or "" (empty strings)
        json_data = df.to_dict(orient='records')

        # Remove "header." and "lineitem." from TargetField
        for record in json_data:
            if "TargetField" in record and isinstance(record["TargetField"], str):
                record["TargetField"] = (record["TargetField"].replace("header.", "").replace("lineitem.", ""))

        return json_data
    except Exception as e:
        raise RuntimeError(f"Error processing file '{csv_file}': {str(e)}")

def convert_json_to_csv(extracted_data, folder_path: str, file_name: str):
    # Ensure directory exists
    ensure_directory_exists(folder_path)

    # Remove existing files in the folder
    for existing_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, existing_file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Create and save the new CSV file
    csv_file_path = os.path.join(folder_path, file_name)
    try:
        df = pd.DataFrame(extracted_data)
        df.to_csv(csv_file_path, index=False)
        return {"message": f"CSV file saved at {csv_file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save CSV: {str(e)}")
