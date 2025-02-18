from dotenv import load_dotenv
from .ZohoBooksInterface import ZohoBooksInterface
from datetime import datetime
import os
load_dotenv(".env")

REFRESH_TOKEN = os.environ.get("ZOHOBOOKS_REFRESH_TOKEN")
CLIENT_ID = os.environ.get("ZOHOBOOKS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ZOHOBOOKS_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("ZOHOBOOKS_REDIRECT_URI")
ORGANIZATION_ID = os.environ.get("ZOHOBOOKS_ORGANIZATION_ID")


zohoBooksClient = ZohoBooksInterface(refresh_token=REFRESH_TOKEN,
                                     client_id=CLIENT_ID,
                                     client_secret=CLIENT_SECRET,
                                     redirect_uri=REDIRECT_URI,
                                     organization_id=ORGANIZATION_ID)

# invoice_data = {
#         "customer_id": 897139000000019825,
#         "invoice_number": "INVOICE-TEST-01",
#         "place_of_supply": "TN",
#         "gst_treatment": "business_gst",
#         "gst_no": "33AALCR3173P1ZU",
#         "date": "2025-01-12",
#         "payment_terms": 0,
#         "payment_terms_label": "Due on Receipt",
#         "is_inclusive_tax": False,
#         "custom_fields": [
#             {
#                 "customfield_id": "897139000015369380", #PO Number
#                 "value": "7VTEZRNB"
#             },
#             {
#                 "customfield_id": "897139000220627280", #Total BoxCount
#                 "value": "1"
#             }
#         ],
#         "line_items": [
#             {
#                 "item_id": 897139000221920724,
#                 "hsn_or_sac": 63079090,
#                 "item_order": 1,
#                 "quantity": 30,
#                 "unit": "pcs",
#                 "rate": 100
#             }
#         ],
#         "notes": "TEST INVOICE DO NOT DO ANYTHING"
#     }
def create_invoice(po_data, customer_data, item_data , x_invoice_number=None):

    '''
        pass po_data        - comes from the PO data
        pass customer_data  - comes from customer_master_data filtered based on the "Display Name" column using purchasing entity from the PO
        pass item_data      -  comes from item_master_data filtered based on the "CF.ASIN" column using "po_line_items.asin" from the PO
        pass x_invoice_number
        if x_invoice_number is not passed, it will autogenerate a invoice_number . For testing pass the invoice number
    '''
    current_date_time = datetime.now().strftime("%Y-%m-%d")
    header_data = {
        "customer_id": customer_data['contact_id'],
        "place_of_supply": po_data['place_of_supply'],
        "gst_treatment": customer_data['gst_treatment'],
        "gst_no": customer_data['gst_identification_number'],
        "date": current_date_time,
        "payment_terms": customer_data['payment_terms'],
        "payment_terms_label": customer_data['payment_terms_label'],
        "is_inclusive_tax": False,
        "custom_fields": [
        {
            "customfield_id": "897139000015369380",  # PO Number
            "value": po_data['po_number']
        },
        {
            "customfield_id": "897139000220627280",  # Total BoxCount
            "value": po_data['total_box_count']
        }
    ]
    }

    line_items_data = []

    for po_line_item in po_data['po_line_items']:
        line_items_data.append({
            "item_id": item_data['item_id'],
            "hsn_or_sac": item_data['hsn_sac'],
            "item_order": 1,
            "quantity": str(po_line_item['qty_requested']),
            "unit": item_data['usage_unit'],
            "rate": str(po_line_item['unit_cost'])
        })
    
    if x_invoice_number:
        header_data['invoice_number'] = x_invoice_number
        invoice_data = {
            **header_data,
            "line_items": line_items_data,
      }
        x_should_ignore_auto_number_generation = True
    else:
      invoice_data = {
            **header_data,
            "line_items": line_items_data,
      } 
      x_should_ignore_auto_number_generation = False 

    status , generated_invoice = zohoBooksClient.create_invoice(invoice_detail=invoice_data,
                                                       should_ignore_auto_number_generation=x_should_ignore_auto_number_generation)
    if status == "SX":
        if generated_invoice['code'] == 0:
            invoice_id = generated_invoice['invoice']['invoice_id']
            invoice_number =  generated_invoice['invoice']['invoice_number']
            status, pdf_content = zohoBooksClient.download_invoice_pdf(invoice_id)
            if status == "SX":
                return "success", generated_invoice['invoice'] , pdf_content
            else:
                return "error" , pdf_content , None
        else:
            message = f"Error in generating the invoice : {generated_invoice['code']} , {generated_invoice['message']}"
            return "error" , message , None
    else:
        return "error" , generated_invoice , None