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

INSERT_PURCHASE_ORDER_LINE_ITEM = """
    INSERT INTO
        evenflow_purchase_orders_line_items (
            evenflow_purchase_orders_id, external_id, model_number, hsn,
            title, window_type, expected_date, qty_requested,
            qty_accepted, qty_received, qty_outstanding, unit_cost,
            total_cost, active_flag, created_by
        )
        VALUES (
            :evenflowPurchaseOrdersId, :externalId, :modelNumber, :hsn,
            :title, :windowType, :expectedDate, :qtyRequested,
            :qtyAccepted, :qtyReceived, :qtyOutstanding, :unitCost,
            :totalCost, :activeFlag, :createdBy
        )
    
"""