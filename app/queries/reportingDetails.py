GET_PURCHASE_ORDER_AGG_DETAILS = """
    SELECT 
        * 
    FROM 
        evenflow_agg_purchase_orders
    WHERE
        active_flag = 1
"""

GET_PURCHASE_ORDER_TOP_CUSTOMERS_AGG_DETAILS = """
    SELECT 
        *
    FROM
        evenflow_agg_purchase_orders_top_customers
    WHERE
        active_flag = 1
"""

GET_INVOICES_AGG_DETAILS = """
    SELECT 
        *
    FROM
        evenflow_agg_invoices
    WHERE
        active_flag = 1
"""

GET_PO_COUNT_DETAILS = """
    SELECT 
        COUNT(*) AS receivedCount, 
        COUNT(CASE WHEN po_processing_status = 'FULFILLED' THEN 1 END) AS fulfilledCount,
        COUNT(CASE WHEN po_processing_status = 'PARTIALLY_FULFILLED' THEN 1 END) AS partiallyFulfilledCount,
        COUNT(CASE WHEN po_processing_status = 'OPEN' THEN 1 END) AS openCount
    FROM
        evenflow_purchase_orders
    WHERE
        active_flag = 1
"""

GET_INVOICES_TOP_CUSTOMERS_AGG_DETAILS = """
    SELECT 
        *
    FROM
        evenflow_agg_invoices_top_customers
    WHERE
        active_flag = 1
"""