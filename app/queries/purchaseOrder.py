GET_PURCHASE_ORDER_DETAILS = """
    SELECT 
        id as evenflow_purchase_orders_id,
        ordered_on, po_file_path
    FROM 
        evenflow_purchase_orders 
    WHERE 
        po_number = '{po_number}'
"""

CHECK_PURCHASE_ORDER_EXIST = """
    SELECT 
        id 
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

INSERT_PURCHASE_ORDER_DETAILS = """
    INSERT INTO 
        evenflow_purchase_orders (
            client_id, evenflow_customer_master_id, total_qty_requested,
            po_number, po_status, vendor, ship_to_location,
            ordered_on, ship_window_from, ship_window_to, freight_terms,
            payment_method, payment_terms, purchasing_entity, submitted_items,
            submitted_qty, submitted_total_cost, accepted_items, accepted_qty,
            accepted_total_cost, cancelled_items, cancelled_qty, cancelled_total_cost,
            received_items, received_qty, received_total_cost, delivery_address_to,
            delivery_address, fiscal_quarter, po_month, po_year,
            active_flag, created_by
        )
        VALUES (
            :clientId, :evenflowCustomerMasterId, :toalRequestedItems,
            :poNumber, :poStatus, :vendor, :shipToLocation,
            :orderedOn, :shipWindowFrom, :shipWindowTo, :freightTerms,
            :paymentMethod, :paymentTerms, :purchasingEntity, :submittedItems,
            :submittedQty, :submittedTotalCost, :acceptedItems, :acceptedQty,
            :acceptedTotalCost, :cancelledItems, :cancelledQty, :cancelledTotalCost,
            :receivedItems, :receivedQty, :receivedTotalCost, :deliveryAddressTo,
            :deliveryAddress, :fiscalQuarter, :poMonth, :poYear,
            :activeFlag, :createdBy
        )
"""


