GET_PURCHASE_ORDER_LINE_ITEM = """
    SELECT 
        qty_requested as quantity, expected_date
    FROM 
        evenflow_purchase_orders_line_items
    WHERE
        evenflow_purchase_orders_id = '{order_id}' and 
        model_number = '{sku}'
"""