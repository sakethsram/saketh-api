GET_PURCHASE_ORDER_LINE_ITEM = """
    SELECT 
        qty_requested as quantity, expected_date
    FROM 
        evenflow_purchase_orders_line_items
    WHERE
        evenflow_purchase_orders_id = '{order_id}' and 
        model_number = '{sku}'
"""

UPDATE_PURCHASE_ORDER_LINE_ITEM = """
    UPDATE 
        evenflow_purchase_orders_line_items
    SET
        po_line_item_processing_status = '{po_status}'
    WHERE
        evenflow_purchase_orders_id = '{purchase_orders_id}' and
        model_number = '{sku}'
"""