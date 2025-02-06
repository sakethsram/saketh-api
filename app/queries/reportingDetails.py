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

PO_TREND_CHART_DAILY_QUERY = """
    SELECT 
        po_date as date, sum(received_po) as no_of_po, sum(received_po_amount) as amount 
    FROM
        evenflow_agg_purchase_orders
    WHERE
        po_date >= '{startDate}' and po_date <= '{endDate}' 
    GROUP BY
        po_date
    ORDER BY 
        po_date 
    DESC
"""

PO_TREND_CHART_MONTHLY_QUERY = """
    SELECT 
        TO_CHAR(DATE_TRUNC('month', po_date), 'Mon, YYYY') AS month, SUM(received_po) AS no_of_po, SUM(received_po_amount) AS amount
    FROM 
        evenflow_agg_purchase_orders
    WHERE 
        DATE_TRUNC('month', po_date) >= DATE_TRUNC('month', '{startDate}'::DATE) 
        AND DATE_TRUNC('month', po_date) <= DATE_TRUNC('month', '{endDate}'::DATE)
    GROUP BY 
        DATE_TRUNC('month', po_date)
    ORDER BY 
        DATE_TRUNC('month', po_date) DESC;
"""

PO_TREND_CHART_QUARTERLY_QUERY = """
    SELECT 
        'Q' || CASE
                  WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN 4
                  WHEN EXTRACT(MONTH FROM po_date) IN (4, 5, 6) THEN 1
                  WHEN EXTRACT(MONTH FROM po_date) IN (7, 8, 9) THEN 2
                  WHEN EXTRACT(MONTH FROM po_date) IN (10, 11, 12) THEN 3
              END || ', ' || CASE
                              WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM po_date) - 1
                              ELSE EXTRACT(YEAR FROM po_date)
                          END AS quarter,
        SUM(received_po) AS no_of_po,
        SUM(received_po_amount) AS amount
    FROM 
        evenflow_agg_purchase_orders
    WHERE 
        po_date >= '{startDate}'::DATE 
        AND po_date <= '{endDate}'::DATE
    GROUP BY 
        CASE
            WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN 4
            WHEN EXTRACT(MONTH FROM po_date) IN (4, 5, 6) THEN 1
            WHEN EXTRACT(MONTH FROM po_date) IN (7, 8, 9) THEN 2
            WHEN EXTRACT(MONTH FROM po_date) IN (10, 11, 12) THEN 3
        END,
        CASE
            WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM po_date) - 1
            ELSE EXTRACT(YEAR FROM po_date)
        END
    ORDER BY 
        CASE
            WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM po_date) - 1
            ELSE EXTRACT(YEAR FROM po_date)
        END DESC,
        CASE
            WHEN EXTRACT(MONTH FROM po_date) IN (1, 2, 3) THEN 4
            WHEN EXTRACT(MONTH FROM po_date) IN (4, 5, 6) THEN 1
            WHEN EXTRACT(MONTH FROM po_date) IN (7, 8, 9) THEN 2
            WHEN EXTRACT(MONTH FROM po_date) IN (10, 11, 12) THEN 3
        END DESC;

"""

PO_TREND_CHART_YEARLY_QUERY = """
    SELECT 
        TO_CHAR(DATE_TRUNC('year', po_date), 'YYYY') AS year, 
        SUM(received_po) AS no_of_po, 
        SUM(received_po_amount) AS amount
    FROM 
        evenflow_agg_purchase_orders
    WHERE 
        DATE_TRUNC('year', po_date) >= DATE_TRUNC('year', '{startDate}'::DATE) 
        AND DATE_TRUNC('year', po_date) <= DATE_TRUNC('year', '{endDate}'::DATE)
    GROUP BY 
        DATE_TRUNC('year', po_date)
    ORDER BY 
        DATE_TRUNC('year', po_date) DESC;

"""