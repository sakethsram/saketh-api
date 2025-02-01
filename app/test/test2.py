from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from typing import List
from app.dependencies import get_db
from app.models import User
from app.models import EvenflowAccountingDetails
from app.models import EvenflowDistys
from app.schemas import EvenFlowAccountingDetailsSchema
from app.schemas import ClientOnboardRequest
from pprint import pprint
import pandas as pd

router = APIRouter()

def dump_body(mapping_items):
    return [item.dict() for item in mapping_items]

def write_po_mappings(df, dfile):
    return
    df.to_excel(dfile, index=False)

def onboard_client_acccount(current_user, cdetails, accdetails):
    client_acc_details = EvenflowAccountingDetails(
        client_id=cdetails.id,
        invoice_inputs="PO",
        invoice_number_auto=True,
        accounting_tool_name=cdetails.accountingtool,
        accounting_tool_url=accdetails.url,
        accounting_tool_userid=accdetails.username,
        accounting_tool_pwd=accdetails.password,
        created_by=current_user,
        modified_by=current_user,
        active_flag=True
    )
    
    print()
    print("Client Account details...")
    instance_dict = {key: value for key, value in client_acc_details.__dict__.items() if not key.startswith('_')}
    print(f"instance_dict :{instance_dict}")
    print()
    
    # db.add(client_acc_details)
    # db.commit()
    # db.refresh(client_acc_details)
    
def onboard_distributors(current_user, cdetails, distributors):
    distys_instances = [
        EvenflowDistys(
            client_id=cdetails.id,
            disty_id=disty_id,
            created_by=current_user,
            modified_by=current_user,
            active_flag=1
        )
        for disty_id in distributors
    ]
    # db.bulk_save_objects(distys_instances)
    # db.commit()
    
    print("Client Distributors details...")
    for instance in distys_instances:
        pprint(vars(instance))
    print()

def update_mappings(mapping, dest_mapping_file):
    for d in mapping:
        print(d)
    df = pd.DataFrame(mapping)
    df.rename(columns={
        'sourceField': 'SourceField',
        'targetField': 'TargetField',
        'value': 'SampleValue'
    }, inplace=True)

    print(df)
    print()
    write_po_mappings(df, dest_mapping_file)

@router.post("/client_onboard")
def client_onboard(
    request: ClientOnboardRequest,
    db: Session = Depends(get_db)
):
    # Access the parsed client_details
    cdetails = request.client_details
    distributors = cdetails.distributors
    accdetails = cdetails.accountingDetails
    pomapping = request.po_mapping
    immapping = request.itemmaster_mapping
    cmapping  = request.customermaster_mapping
    
    print(f"cdetails      :{cdetails}")
    print(f"distributors  :{cdetails.distributors}")
    print(f"accdetails    :{accdetails}")
    print(f"pomapping     :{dump_body(pomapping)}")
    print(f"immapping     :{dump_body(immapping)}")
    print(f"cmapping      :{dump_body(cmapping)}")
    
    # =============== client account details ============= 
    onboard_client_acccount("current_user", cdetails, accdetails)
        
    # =============== client distributors details ============= 
    onboard_distributors("current_user", cdetails, distributors)
    
    # =============== po mappings details ============= 
    print("PO Mappings...")
    po_mapping_file = "po_mapping.xlsx"
    update_mappings(pomapping, po_mapping_file)

    # =============== item master mappings details ============= 
    print("Item Master mapping...")
    im_mapping_file = "itemmaster_mapping.xlsx"
    update_mappings(immapping, im_mapping_file)

    # =============== item master mappings details ============= 
    print("Customer Master mapping...")
    cm_mapping_file = "custmaster_mapping.xlsx"
    update_mappings(cmapping, cm_mapping_file)
    
    return {"message": "Client onboarded successfully"}
