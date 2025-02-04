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
        purchasing_entity, count(*) as po_count, TO_CHAR(sum(received_total_cost),'FM999999999.00') as po_amount 
    FROM
        evenflow_purchase_orders
    GROUP BY 
        purchasing_entity
    ORDER BY 
        sum(received_total_cost) DESC 
    LIMIT 
        5;
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
        COUNT(*) AS received_Count, 
        COUNT(CASE WHEN po_processing_status = 'FULFILLED' THEN 1 END) AS fulfilled_Count,
        COUNT(CASE WHEN po_processing_status = 'PARTIALLY_FULFILLED' THEN 1 END) AS partiallyFulfilled_Count,
        COUNT(CASE WHEN po_processing_status = 'OPEN' THEN 1 END) AS open_Count
    FROM
        evenflow_purchase_orders
    WHERE
        active_flag = 1
"""

TOP_5_CUSTOMERS_BASED_ON_PO_COUNT = """
    SELECT 
        purchasing_entity, count(*) as po_count 
    FROM 
        evenflow_purchase_orders
    GROUP BY 
        purchasing_entity
    order by 
        count(*) desc 
    LIMIT 
        5;

"""

GET_PRICE_DETAILS_FOR_KPI = """
    SELECT
        SUM(CASE WHEN po_processing_status = 'FULFILLED' THEN received_total_cost ELSE 0 END) AS fulfilled_Price,
        SUM(CASE WHEN po_processing_status = 'OPEN' THEN received_total_cost ELSE 0 END) AS open_Price,
		SUM(CASE WHEN po_processing_status = 'PARTIALLY_FULFILLED' THEN received_total_cost ELSE 0 END) AS partiallyFulfilled_Price,
		SUM(received_total_cost) AS total_Price
    FROM 
        evenflow_purchase_orders;
"""


AGG_PURCHASE_ORDER_TOP_CUSTOMER  ="""
    SELECT
        * 
    FROM 
        evenflow_agg_purchase_orders_top_customers
    ORDER BY
        po_year, po_qtr 
    DESC 
    LIMIT 
        4;
"""
