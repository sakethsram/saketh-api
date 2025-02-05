import re
import fitz
import pandas as pd
from loguru import logger
from datetime import datetime
from dateutil import parser

class ExtractPOData:
    _patterns = {
        'po_number': re.compile(r"PO:\s+(\w+)",re.IGNORECASE),
        'delivery_address': re.compile(r"Delivery Address:\s+(\w+)",re.IGNORECASE),
        'po_item_number': re.compile(r"PO items\s+\((\d+)\)",re.IGNORECASE)
        }
        #key for which newline should be removed
    _normalize_newline_in_key_value_pairs =  ['ASIN', 'External Id','Model Number','HSN','Cancella\ntion\nstatus','Cancella\ntion\ndate']


    @staticmethod
    def extract_tabular_data(pdf_path):
        """
        Extracts tables from a PDF file and converts them into pandas DataFrames.

        Parameters
        ----------
        pdf_path : str
            Path to the PDF file.

        Returns
        -------
        list
            A list of extracted tables, where each table is represented as a pandas DataFrame.
        """
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
        """
        Extracts text blocks from a PDF file and attempts to split the text into columns.

        Parameters
        ----------
        pdf_path : str
            Path to the PDF file.

        Returns
        -------
        list
            A list of extracted text blocks, where each block is represented as a list of columns.
        """
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
    
    @staticmethod
    def convert_to_yyyy_mm_dd(date_string):
        try:
            parsed_date = parser.parse(date_string)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            return "Invalid date format"
    
    @staticmethod
    def get_platform_key(key_mapper,field_name:str):
        """
        Maps a PDF field name to a target application field name using a key mapper DataFrame.
        
        Parameters
        ----------
        key_mapper : pandas.DataFrame
            A DataFrame with two columns (SourceField, TargetField) that maps the PDF fields to the target application fields.
        field_name : str
            The PDF field name to be mapped.
        
        Returns
        -------
        str
            The target application field name.
        """
        try:
            platform_key = key_mapper.loc[key_mapper["SourceField"].str.lower() == field_name.lower()]["TargetField"].values[0].split(".")[-1]
        except:
            #print(f"Error getting platform_key for {field_name} . using field_name as is")
            platform_key = field_name.lower().replace("\n","").replace(" ","_")
        return platform_key
    
    def extract_po_data(po_file_path:str,key_mapper)->dict:
        
        """
        Reads a PO PDF file and a mapping csv file and returns a dictionary of extracted data.
        
        Parameters
        ----------
        po_file_path : str
            Path to the PO PDF file.
        key_mapper : pandas.DataFrame
            A DataFrame with two columns (SourceField, TargetField) that maps the PDF fields to the target application fields.
        
        Returns
        -------
        dict
            A dictionary with the extracted data.
        """
        output_key_value = {}

        blocks = ExtractPOData.extract_block_data(po_file_path)
        tables = ExtractPOData.extract_tabular_data(po_file_path)

        # extract required data from blocks
        for block_index, block in enumerate(blocks):
            for i,row in enumerate(block):
                if "PO:" in row[0]:
                    match = ExtractPOData._patterns["po_number"].search(row[0])
                    tkey = ExtractPOData.get_platform_key(key_mapper,'PO')
                    output_key_value[tkey] = match.group(1)

                if "Delivery Address:" in row[0]:
                    match = ExtractPOData._patterns["delivery_address"].search(row[0])
                    tkey = ExtractPOData.get_platform_key(key_mapper,'Delivery Address To')
                    output_key_value[tkey] = match.group(1)
                    tkey = ExtractPOData.get_platform_key(key_mapper,'Delivery Address')
                    output_key_value[tkey]= block[i+1][0]
                
                if "PO items" in row[0]:
                    match = ExtractPOData._patterns["po_item_number"].search(row[0])
                    output_key_value['no_of_po_items'] = match.group(1)
        
        #logger.info(f"Number of tables :{len(tables)}")
        
        po_line_items = []

        # extract the required data from tables
        for tables_index, table in enumerate(tables):
            
            df: pd.DataFrame =  table
            
            #logger.info(f"Headers: {df.columns.to_list()}")
            #logger.info(f"No of Rows: {len(df)}")
            
            #header-on-right
            if 'Status' in df.columns:
                df.loc[-1] = df.columns.to_list() 
                df = df.sort_index().reset_index(drop=True)
                df.columns = ['key', 'value']
                
                for i, row in  df.iterrows():
                    if row['key'] == 'Ship window':
                        ship_window_from = row['value'].split('-')[0].strip()
                        ship_window_from = ExtractPOData.convert_to_yyyy_mm_dd(ship_window_from)
                        #ship_window_from = datetime.strptime(ship_window_from, "%d/%m/%Y").strftime("%Y-%m-%d")

                        ship_window_to = row['value'].split('-')[1].strip()
                        ship_window_to = ExtractPOData.convert_to_yyyy_mm_dd(ship_window_to)
                        #ship_window_to = datetime.strptime(ship_window_to, "%d/%m/%Y").strftime("%Y-%m-%d")
                        
                        output_key_value['ship_window_from'] = ship_window_from
                        output_key_value['ship_window_to'] = ship_window_to
                    else:
                        tkey = ExtractPOData.get_platform_key(key_mapper,row['key'])
                        output_key_value[tkey] = row['value']

            #header-on-left
            if 'Items' in df.columns:
                records = df.to_dict(orient='records')
                for record in records:
                    header = record['Col0']
                    for key, value in record.items():
                        if key != 'Col0':
                            tkey = ExtractPOData.get_platform_key(key_mapper,header + " (" + key + ")")
                            output_key_value[tkey] = value
            

            # Get PO ITEMS DATA
            if 'ASIN' in df.columns:
                records = df.to_dict(orient='records')
                for record in records:
                    normalized_record = {}
                    for key, value in record.items():
                        if key in  ExtractPOData._normalize_newline_in_key_value_pairs:
                            normalized_key = key.replace("\n"," ")
                            tkey = ExtractPOData.get_platform_key(key_mapper,normalized_key)
                            normalized_record[tkey] = value.replace("\n","")
                        else:
                            normalized_key = key.replace("\n"," ")
                            tkey = ExtractPOData.get_platform_key(key_mapper,normalized_key)
                            normalized_record[tkey] = value.replace("\n"," ")
                    
                    records[records.index(record)] = normalized_record
                po_line_items.extend(records)
                
        output_key_value['po_line_items'] = po_line_items
        return output_key_value

    def get_data_from_po(po_file_path:str , po_mapping_file_path:str)->dict:   
        """
        Reads a PO PDF file and a mapping csv file and returns a dictionary of extracted data.
        
        Parameters
        ----------
        po_file_path : str
            Path to the PO PDF file.
        po_mapping_file_path : str
            Path to the mapping csv file.
        
        Returns
        -------
        dict
            A dictionary with the extracted data.
        """
        po_key_map_data = pd.read_csv(po_mapping_file_path,header=0)  
        po_data = ExtractPOData.extract_po_data(po_file_path=po_file_path, key_mapper=po_key_map_data) 
        #print(json.dumps(po_data,indent=4)) 
        return po_data

# po_file_path = r"D:\3.Freelancing\Sudhakar\INVOICE_GENERATION_B2B_USECASE\po_data_extraction\Data\Input\1MW85B4B.pdf"
# mapping_file_path = r"C:\Users\saina\Downloads\drive-download-20250129T035146Z-001\evenflow-po-mappings.csv"
# ExtractPOData.get_data_from_po(po_file_path=po_file_path,po_mapping_file_path=mapping_file_path)