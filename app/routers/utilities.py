from fastapi import UploadFile
import os
import json
import shutil
import hashlib
import pandas as pd
from datetime import datetime
from app.config.config import settings

def convert_csv_to_json(page_id):
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


