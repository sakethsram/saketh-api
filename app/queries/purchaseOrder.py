GET_PURCHASE_ORDER_DETAILS = """
    SELECT 
        id as evenflow_purchase_orders_id,
        ordered_on, po_file_path
    FROM 
        evenflow_purchase_orders 
    WHERE 
        po_number = '{po_number}'
"""

UPDATE_PURCHASE_ORDER_DETAILS = """
    UPDATE
        evenflow_purchase_orders
    SET 
        po_processing_status = '{po_status}'
    WHERE
        po_number = '{po_number}'
"""