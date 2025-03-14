GET_PURCHASE_ORDER_LINE_ITEM = """
    SELECT 
        qty_requested as quantity, expected_date, qty_accepted as acceptedQty
    FROM 
        evenflow_purchase_orders_line_items
    WHERE
        id = '{purchase_order_line_item_id}' and
        active_flag = 1
"""

UPDATE_PURCHASE_ORDER_LINE_ITEM = """
    UPDATE 
        evenflow_purchase_orders_line_items
    SET
        qty_fulfilled = qty_fulfilled + {fulfilledQty},
        po_line_item_processing_status = CASE 
            WHEN qty_accepted = qty_fulfilled + {fulfilledQty} THEN 'FULFILLED'
            ELSE 'PARTIALLY_FULFILLED'
        END
    WHERE
        id = {poLineItemId}
        AND active_flag = 1;
"""

INSERT_PURCHASE_ORDER_LINE_ITEM = """
    INSERT INTO
        evenflow_purchase_orders_line_items (
            evenflow_purchase_orders_id, external_id, model_number, hsn,
            title, window_type, expected_date, qty_requested,
            qty_accepted, qty_received, qty_outstanding, unit_cost,
            total_cost, active_flag, created_by, po_line_item_processing_status,
            asin, qty_fulfilled, modified_by
        )
        VALUES (
            :evenflowPurchaseOrdersId, :externalId, :modelNumber, :hsn,
            :title, :windowType, :expectedDate, :qtyRequested,
            :qtyAccepted, :qtyReceived, :qtyOutstanding, :unitCost,
            :totalCost, :activeFlag, :createdBy, 'OPEN', 
            :asin, 0, :modifiedBy
        )
    
"""