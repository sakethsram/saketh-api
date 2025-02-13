GET_PURCHASE_ORDER_DETAILS = """
    SELECT 
        id as evenflow_purchase_orders_id,
        ordered_on, po_file_path
    FROM 
        evenflow_purchase_orders 
    WHERE 
        po_number = '{po_number}' and
        active_flag = 1
"""

CHECK_PURCHASE_ORDER_EXIST = """
    SELECT 
        id 
    FROM 
        evenflow_purchase_orders 
    WHERE 
        po_number = '{po_number}' and
        active_flag = 1
"""

UPDATE_PURCHASE_ORDER_DETAILS = """
    UPDATE 
        evenflow_purchase_orders EPO
    SET po_processing_status = CASE 
                                WHEN EPO.submitted_qty = EPOLI.lineItemTotalQty THEN 'IN_PROGRESS_FULL'
                                ELSE 'IN_PROGRESS_PARTIAL'
                             END
    FROM (
        SELECT evenflow_purchase_orders_id, COUNT(qty_requested) AS lineItemTotalQty
        FROM evenflow_purchase_orders_line_items where active_flag = 1
        GROUP BY evenflow_purchase_orders_id
    ) EPOLI
    WHERE EPO.id = EPOLI.evenflow_purchase_orders_id
    AND po_number = '{po_number}' AND EPO.active_flag = 1;
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
            active_flag, created_by, po_processing_status, po_file_path, 
            total_qty_accepted, total_qty_fulfilled, total_qty_outstanding
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
            :activeFlag, :createdBy, 'OPEN', :s3Path, 
            :toalQtyAccepted, :totalQtyFullfilled, :totalQtyOutstanding
        )
"""


