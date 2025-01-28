import json

def load_clients(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

class Settings:
    SECRET_KEY = "dataworkx-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    
    # Base folder for storing files
    base_folder = "e_commerce_platform"
    purchase_orders_folder = "purchase_orders"
    item_master_folder = "item_master"
    customer_master_folder = "customer_master"
    sample_po = "sample-po"

    # Folder structure sub-categories
    po_mappings_folder = "po_mappings"
    item_master_mappings_folder = "item_master_mappings"
    customer_master_mappings_folder = "customer_master_mappings"

settings = Settings()


