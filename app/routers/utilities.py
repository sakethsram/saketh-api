from fastapi import UploadFile
import os
import shutil
import hashlib
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

import json

def po_to_json(file_path):
    """
    Simulates the processing of a file and returns sample JSON data.
    Args:
        file_path (str): Path to the file.
    Returns:
        dict: Sample JSON data.
    """
    # Sample JSON data (replace this with the actual logic later)
    sample_json_data = [
  {
    "SourceField": "PO",
    "TargetField": "po_number",
    "SampleValue": "7VTEZRNB"
  },
  {
    "SourceField": "Status",
    "TargetField": "po_status",
    "SampleValue": "Closed"
  },
  {
    "SourceField": "Vendor",
    "TargetField": "vendor",
    "SampleValue": "EV7CR"
  },
  {
    "SourceField": "Ship to Location",
    "TargetField": "ship_to_location",
    "SampleValue": "BLR4 - BENGALURU, KARNATAKA"
  },
  {
    "SourceField": "Ordered On",
    "TargetField": "ordered_on",
    "SampleValue": "11/20/2024"
  },
  {
    "SourceField": "Ship window",
    "TargetField": "ship_window_from",
    "SampleValue": "45617"
  },
  {
    "SourceField": "Ship window",
    "TargetField": "ship_window_to",
    "SampleValue": "45658"
  }
]
    
    return sample_json_data

