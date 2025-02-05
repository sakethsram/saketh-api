from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from typing import List
from app.dependencies import get_db
from app.models import User
from app.models import ClientMaster
from app.models import DistyMaster
from app.schemas import ClientMasterSchema
from app.security import validate_token
from app.schemas import AccountingDetailsSchema
from app.models import EvenflowAccountingDetails
from app.models import EvenflowDistys
from app.models import EvenflowCustomerMaster
from app.models import EvenflowProductMaster
from app.schemas import ClientOnboardRequest
from pprint import pprint
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import re
from app.schemas import AccountingToolDetails 
from typing import List 
from sqlalchemy.exc import SQLAlchemyError
import logging

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/get_clients", response_model=List[ClientMasterSchema])
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme), 
    authorization: str = Header(None, description="Bearer token for authentication")
    ):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db) 

    clients = db.query(ClientMaster).all()
    if not clients:raise HTTPException(status_code=404, detail="Clients not found")
    
    return [ClientMasterSchema(id=client.id,name=client.name) for client in clients]


@router.get("/account-details", response_model=List[dict])
def get_accounting_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = validate_token(token, db)

    # Query the database for accounting details
    accounting_details = (
        db.query(EvenflowAccountingDetails)
        .filter(EvenflowAccountingDetails.active_flag == 1)
        .all()
    )

    if not accounting_details:
        raise HTTPException(status_code=404, detail="Accounting Details not found")

    # Transform response to match required format
    return [
        {
            "id": detail.id,
            "accountingToolName": detail.accounting_tool_name  # Convert to camelCase
        }
        for detail in accounting_details
    ]

def dump_body(mapping_items):
    return [item.dict() for item in mapping_items]

def write_po_mappings(df, dfile):
    df.to_excel(dfile, index=False)
    print(f"File written: {dfile}")
    return

def onboard_distributors(db: Session, current_user: str, cdetails: object, distributors: list):
    try:
        # Validate input
        if not hasattr(cdetails, 'id'):
            raise ValueError("cdetails must have an 'id' attribute.")
        if not isinstance(distributors, (list, tuple)):
            raise ValueError("distributors must be a list or tuple.")

        # Fetch distributor details from disty_master table
        disty_records = db.query(DistyMaster).filter(DistyMaster.id.in_(distributors)).all()

        if not disty_records:
            raise ValueError("No distributors found with the provided IDs.")

        logging.debug(f"Fetched distributor records: {[d.id for d in disty_records]}")

        # Prepare distributor instances for insertion into EvenflowDistys
        distys_instances = []
        for disty in disty_records:
            # Check if the distributor already exists in EvenflowDistys to prevent duplicates
            existing_record = db.query(EvenflowDistys).filter_by(client_id=cdetails.id, disty_id=disty.id).first()

            if existing_record:
                logging.debug(f"Distributor ID {disty.id} already exists for client {cdetails.id}, skipping.")
                continue

            new_disty = EvenflowDistys(
                client_id=cdetails.id,
                disty_id=disty.id,
                created_by=current_user,
                modified_by=current_user,
                active_flag=1
            )

            distys_instances.append(new_disty)

        # Bulk insert distributors into EvenflowDistys table
        if distys_instances:
            logging.debug(f"Inserting distributors: {[d.disty_id for d in distys_instances]}")
            db.bulk_save_objects(distys_instances)
            db.flush()  # Ensure data is written before commit
            db.commit()  # Commit the transaction

            logging.info(f"Inserted {len(distys_instances)} new distributors into EvenflowDistys.")

        else:
            logging.info("No new distributors to add.")

    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error occurred: {str(e)}")
        raise
    except ValueError as e:
        logging.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        raise
    finally:
        db.close()


def onboard_client_acccount(db, current_user, cdetails, accdetails):
    try:
        # Validate input
        if not hasattr(cdetails, 'id') or not hasattr(cdetails, 'accountingtool'):
            raise ValueError("cdetails must have 'id' and 'accountingtool' attributes.")
        if not hasattr(accdetails, 'url') or not hasattr(accdetails, 'username') or not hasattr(accdetails, 'password'):
            raise ValueError("accdetails must have 'url', 'username', and 'password' attributes.")

        # Convert URL to string
        accounting_tool_url = str(accdetails.url) if accdetails.url else None

        # Create an instance of EvenflowAccountingDetails
        client_acc_details = EvenflowAccountingDetails(
            client_id=cdetails.id,
            invoice_inputs="PO",  # Example hardcoded value, adjust if necessary
            invoice_number_auto=1,  # Use 1 for True (SMALLINT compatibility)
            accounting_tool_name=cdetails.accountingtool,
            accounting_tool_url=accounting_tool_url,  # Ensure this is a string
            accounting_tool_userid=accdetails.username,
            accounting_tool_pwd=accdetails.password,
            created_by=current_user,
            modified_by=current_user,
            active_flag=1  # Use 1 for True (SMALLINT compatibility)
        )

        # Log the details of the instance
        print("\nClient Account details...")
        instance_dict = {key: value for key, value in client_acc_details.__dict__.items() if not key.startswith('_')}
        print(f"instance_dict: {instance_dict}\n")

        # Add to the database and commit
        db.add(client_acc_details)
        db.commit()
        db.refresh(client_acc_details)

    except SQLAlchemyError as e:
        # Rollback the transaction on database error
        db.rollback()
        print(f"Database error occurred: {str(e)}")
    except ValueError as e:
        # Handle validation errors
        print(f"Validation error: {str(e)}")
    finally:
        # Close the session if applicable
        db.close()
    
def po_update_mappings(mapping):
    po_mapping_file = "po_mapping.xlsx"

    transformed_data = []
    for entry in mapping:
        print(entry)
        transformed_data.append({
            "SourceField": entry.sourceField,
            "TargetField": entry.targetField.split('.')[-1],
            "SampleValue": entry.value
      })

    df = pd.DataFrame(transformed_data)

    print(df)
    print()

    write_po_mappings(df, po_mapping_file)


def update_customer_master_table(db: Session, current_user: str, client_id: int, customer_data):
    try:
        if isinstance(customer_data, list):
            customer_data = pd.DataFrame(customer_data)

        if not isinstance(customer_data, pd.DataFrame):
            raise ValueError("customer_data must be a Pandas DataFrame or a list of dictionaries")

        print("Columns in customer_data:", customer_data.columns)

        if 'TargetField' not in customer_data.columns or 'SampleValue' not in customer_data.columns:
            raise KeyError("Missing required columns: 'TargetField' or 'SampleValue' in customer_data")

        data_to_insert = {'client_id': client_id, 'created_by': current_user, 'modified_by': current_user}

        for _, row in customer_data.iterrows():
            target_field = row['TargetField']
            sample_value = row['SampleValue']
            
            # Skip rows with no value, "No value", or where TargetField is '-'
            if not sample_value or sample_value == "No value" or target_field.strip() == "-":
                continue

            # Map 'status' to 'active_flag'
            if target_field.lower() == 'status':
                target_field = 'active_flag'
                sample_value = 1 if str(sample_value).strip().lower() in ['active', '1', 'yes', 'true'] else 0

            # Convert specific SMALLINT fields to integers
            if target_field in ['bank_account_payment', 'credit_limit', 'taxable', 'active_flag']:
                sample_value = 1 if str(sample_value).strip().lower() in ['true', '1', 'yes', 'active'] else 0

            # Sanitize the column name (replace invalid characters with '_')
            sanitized_target_field = re.sub(r'[^a-zA-Z0-9_]', '_', target_field)

            data_to_insert[sanitized_target_field] = sample_value

        customer_instance = EvenflowCustomerMaster(**data_to_insert)

        db.add(customer_instance)
        db.commit()

        print(f"Inserted customer data: {data_to_insert}")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {str(e)}")
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        print("Ensure the DataFrame contains 'TargetField' and 'SampleValue' columns.")
    except ValueError as e:
        print(f"Validation error: {str(e)}")
    finally:
        # Ensure the database session is properly closed
        db.close()


def update_item_master_table(db: Session, current_user: str, client_id: int, product_data):
    import pandas as pd
    import re

    try:
        if isinstance(product_data, list):
            product_data = pd.DataFrame(product_data)

        if not isinstance(product_data, pd.DataFrame):
            raise ValueError("product_data must be a Pandas DataFrame or a list of dictionaries")

        print("Columns in product_data:", product_data.columns)

        data_to_insert = {'client_id': client_id, 'created_by': current_user, 'modified_by': current_user}

        for _, row in product_data.iterrows():
            target_field = row['TargetField']
            sample_value = row['SampleValue']
            
            # Skip rows with no value, "No value", or where TargetField is '-'
            if not sample_value or sample_value == "No value" or target_field.strip() == "-":
                continue

            # Map 'status' to 'active_flag'
            if target_field.lower() == 'status':
                target_field = 'active_flag'
                sample_value = 1 if str(sample_value).strip().lower() in ['active', '1', 'yes', 'true'] else 0

            # Convert specific SMALLINT fields to integers
            if target_field in ['taxable', 'is_combo_product', 'active_flag']:
                sample_value = 1 if str(sample_value).strip().lower() in ['true', '1', 'yes', 'active'] else 0

            # Handle DECIMAL fields (clean and convert to float or Decimal)
            if target_field in [
                'rate', 'intra_state_tax_rate', 'inter_state_tax_rate', 'purchase_rate',
                'reorder_point', 'opening_stock', 'opening_stock_value', 'stock_on_hand',
                'cf_az_tp_excl_gst', 'cf_mrp_with_tax', 'cf_fk_tp_excl_gst', 'cf_instamart_tp_excl_gst',
                'cf_blinkit_tp'
            ]:
                # Use regex to extract numeric value
                match = re.search(r'[\d.]+', str(sample_value))
                sample_value = float(match.group()) if match else 0.0

            # Sanitize the column name (replace invalid characters with '_')
            sanitized_target_field = re.sub(r'[^a-zA-Z0-9_]', '_', target_field)

            data_to_insert[sanitized_target_field] = sample_value

        # Create an instance of the ORM model using the sanitized dictionary
        product_instance = EvenflowProductMaster(**data_to_insert)

        db.add(product_instance)
        db.commit()

        print(f"Inserted product data: {data_to_insert}")

    except SQLAlchemyError as e:
        # Rollback the transaction if an error occurs
        db.rollback()
        print(f"Database error occurred: {str(e)}")
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        print("Ensure the DataFrame contains 'TargetField' and 'SampleValue' columns.")
    except ValueError as e:
        print(f"Validation error: {str(e)}")
    finally:
        db.close()

def cm_update_mappings(db, current_user, client_id, mapping):
    cm_mapping_file = "custmaster_mapping.xlsx"
    
    transformed_data = []
    for entry in mapping:
        print(entry)
        transformed_data.append({
            "SourceField": entry.sourceField,
            "TargetField": entry.targetField.split('.')[-1],
            "SampleValue": entry.value
      })

    df = pd.DataFrame(transformed_data)

    print(df)
    print()

    write_po_mappings(df, cm_mapping_file)
    update_customer_master_table(db, current_user, client_id, df)

def im_update_mappings(db, current_user, client_id, mapping):
    im_mapping_file = "itemmaster_mapping.xlsx"

    transformed_data = []
    for entry in mapping:
        print(entry)
        transformed_data.append({
            "SourceField": entry.sourceField,
            "TargetField": entry.targetField.split('.')[-1],
            "SampleValue": entry.value
      })

    df = pd.DataFrame(transformed_data)

    print(df)
    print()

    write_po_mappings(df, im_mapping_file)
    update_item_master_table(db, current_user, client_id, df)
    
@router.post("/client_onboard")
def client_onboard(
    request: ClientOnboardRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    print(f"==========current_user :{current_user}")
    current_user = "bhagavan"
    # Access the parsed client_details
    cdetails = request.client_details
    distributors = cdetails.distributors
    accdetails = cdetails.accountingDetails
    pomapping = request.po_mapping
    immapping = request.itemmaster_mapping
    cmapping  = request.customermaster_mapping
    
    print(f"cdetails      :{cdetails}")
    print(f"distributors  :{cdetails.distributors}")
    # print(f"accdetails    :{accdetails}")
    # print(f"pomapping     :{dump_body(pomapping)}")
    # print(f"cmapping      :{dump_body(cmapping)}")
    # print(f"immapping     :{dump_body(immapping)}")
    
    # =============== client distributors details =============
    onboard_distributors(db, current_user, cdetails, distributors)

    # =============== client account details =============
    onboard_client_acccount(db, current_user, cdetails, accdetails)
    
    # =============== po mappings details =============
    print("PO Mappings...")
    po_update_mappings(pomapping)

    # =============== item master mappings details =============
    print("Item Master mapping...")
    cm_update_mappings(db, current_user, cdetails.id, cmapping)

    # =============== item master mappings details =============
    print("Customer Master mapping...")
    im_update_mappings(db, current_user, cdetails.id, immapping)
    return {"message": "Client onboarded successfully"}
    
	# client_onboard, evenflow_distys
	# client_accounting_details, evenflow_accounting_details
	# PO maping --> PO.xls
	# Item_master details --> evenflow_product_master
	# Customer_master details  -->  evenflow_customer_master
 
