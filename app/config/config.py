import json

def load_clients(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

class Settings:
    SECRET_KEY = "dataworkx-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    
    # Base folder for storing files
    purchase_orders_folder = "purchase-orders"
    item_master_folder = "item-master"
    customer_master_folder = "customer-master"
    sample_po = "sample-po"

    # Folder structure sub-categories
    po_mappings_folder = "po-mappings"
    item_master_mappings_folder = "item-master-mappings"
    customer_master_mappings_folder = "customer-master-mappings"

settings = Settings()


