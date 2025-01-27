import re
import os
import json
import fitz
import pandas as pd
from loguru import logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(CURRENT_DIR, "data","input")
OUTPUT_FOLDER = os.path.join(CURRENT_DIR, "data","output")
PATTERNS = {
    'po_number': re.compile(r"PO:\s+(\w+)",re.IGNORECASE),
    'delivery_address': re.compile(r"Delivery Address:\s+(\w+)",re.IGNORECASE),
    'po_item_number': re.compile(r"PO items\s+\((\d+)\)",re.IGNORECASE)
}

#key for which newline should be removed
NORMALIZE_NEWLINE_IN_KEY_VALUE_PAIRS =  ['ASIN', 'External Id','Model Number','HSN','Cancella\ntion\nstatus','Cancella\ntion\ndate']
    
class ExtractData:
    @staticmethod
    def extract_tabular_data(pdf_path):
        pdf_document = fitz.open(pdf_path)
        extracted_tables = []
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            tables = page.find_tables()
            for table in tables:
                # print(table.to_pandas())
                extracted_tables.append(table.to_pandas())

        pdf_document.close()
        return extracted_tables

    @staticmethod
    def extract_block_data(pdf_path):
        # Open the PDF document
        pdf_document = fitz.open(pdf_path)
        extracted_blocks = []
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            blocks = page.get_text("blocks")  
            block_data = []
            for block in blocks:

                # print(block)
                text = block[4].strip()
                if text:
                    # Attempt to split the text into columns
                    columns = text.split('\t') if '\t' in text else text.split('  ')
                    columns = [col.strip() for col in columns if col.strip()]
                    block_data.append(columns)

            if block_data:
                extracted_blocks.append(block_data)

        pdf_document.close()
        return extracted_blocks


def extractData(file_path):

    output_key_value = {}
    blocks = ExtractData.extract_block_data(file_path)
    tables = ExtractData.extract_tabular_data(file_path)

    # extract required data from blocks
    for block_index, block in enumerate(blocks):
        for i,row in enumerate(block):
            if "PO:" in row[0]:
                match = PATTERNS["po_number"].search(row[0])
                output_key_value['po_number'] = match.group(1)

            if "Delivery Address:" in row[0]:
                match = PATTERNS["delivery_address"].search(row[0])
                output_key_value['delivery_address_code'] = match.group(1)
                output_key_value['delivery_address']= block[i+1][0]
            
            if "PO items" in row[0]:
                match = PATTERNS["po_item_number"].search(row[0])
                output_key_value['no_of_po_items'] = match.group(1)
    
    logger.info(f"Number of tables :{len(tables)}")
    
    po_line_items = []

    # extract the required data from tables
    for tables_index, table in enumerate(tables):
        
        df: pd.DataFrame =  table
        
        logger.info(f"Headers: {df.columns.to_list()}")
        logger.info(f"No of Rows: {len(df)}")
        
        #header-on-right
        if 'Status' in df.columns:
            df.loc[-1] = df.columns.to_list() 
            df = df.sort_index().reset_index(drop=True)
            df.columns = ['key', 'value']
            
            for i, row in  df.iterrows():
                output_key_value[row['key'].lower().replace(" ","_")] = row['value']

        #header-on-left
        if 'Items' in df.columns:
            records = df.to_dict(orient='records')
            for record in records:
                header = record['Col0'].lower().replace(" ","_")
                for key, value in record.items():
                    if key != 'Col0':
                        output_key_value[header + "_" + key.lower().replace(" ","_")] = value
        

        #po-items-table
        if 'ASIN' in df.columns:
            records = df.to_dict(orient='records')
            for record in records:
                normalized_record = {}
                for key, value in record.items():
                    if key in  NORMALIZE_NEWLINE_IN_KEY_VALUE_PAIRS:
                        normalized_key = key.lower().replace(" ","_").replace("\n","")
                        normalized_record[normalized_key] = value.replace("\n","")
                    else:
                        normalized_key = key.lower().replace(" ","_").replace("\n","_")
                        normalized_record[normalized_key] = value.replace("\n"," ")
                    
                records[records.index(record)] = normalized_record
            po_line_items.extend(records)
               
    output_key_value['po_line_items'] = po_line_items
    return output_key_value

# if __name__ == "__main__":
    
#     for file in os.listdir(INPUT_FOLDER):
#         try:
#             logger.info(f"Processing file :{file}")
#             if file.endswith(".pdf"):
#                 file_path = os.path.join(INPUT_FOLDER, file)
#                 output = main(file_path)
#                 # if output:
#                 #     with open(os.path.join(OUTPUT_FOLDER, file.replace(".pdf",".json")), 'w') as f:
#                 #         f.write(json.dumps(output,indent=4))
#             logger.info(f"Processed file : {file}")
#         except Exception as e:
#             logger.error(f"Error processing file {file}: {e}")
