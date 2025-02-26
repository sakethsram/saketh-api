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
        5;
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

TOP_5_CUSTOMERS_BASED_ON_INVOIVE_COUNT = """
    SELECT 
        customer_name, count(*) as Invoice_count 
    FROM 
        evenflow_invoices
    GROUP BY 
        customer_name
    order by 
        count(*) desc 
    LIMIT 
        5;

"""

TOP_5_CUSTOMERS_BASED_ON_INVOICE_AMOUNT = """
    SELECT
        customer_name, count(*) as Invoice_count, TO_CHAR(sum(invoice_amount),'FM999999999.00') as po_amount 
    FROM
        evenflow_invoices
    GROUP BY 
        customer_name
    ORDER BY 
        sum(invoice_amount) DESC 
    LIMIT
        5;

"""

AGG_INVOICES_TOP_CUSTOMER  ="""
    SELECT
        * 
    FROM 
        evenflow_agg_invoices_top_customers
    ORDER BY
        invoice_year, invoice_qtr 
    DESC 
    LIMIT
        5;
"""

GET_INVOICE_COUNT_DETAILS_FOR_KPI = """
    SELECT 
        COUNT(*) AS total_Count, 
        COUNT(CASE WHEN invoice_status = 'OVER_DUE' THEN 1 END) AS overdue_Count,
        COUNT(CASE WHEN invoice_status = 'DUE' THEN 1 END) AS due_Count,
        COUNT(CASE WHEN invoice_status = 'TO_BE_GENERATED' THEN 1 END) AS tobegenerated_Count
    FROM
        evenflow_invoices
    WHERE
        active_flag = 1
"""

GET_INVOICE_AMOUNT_DETAILS_FOR_KPI = """
    SELECT
        SUM(CASE WHEN invoice_status = 'OVER_DUE' THEN invoice_amount ELSE 0 END) AS overdue_Amount,
        SUM(CASE WHEN invoice_status = 'DUE' THEN invoice_amount ELSE 0 END) AS due_Amount,
		SUM(CASE WHEN invoice_status = 'TO_BE_GENERATED' THEN invoice_amount ELSE 0 END) AS tobegenerated_Amount,
		SUM(invoice_amount) AS total_Price
    FROM 
        evenflow_invoices;
"""

INVOICE_TREND_CHART_DAILY_QUERY = """
    SELECT 
        invoice_date as date, sum(raised_invoice) as no_of_invoices, sum(raised_invoice_amount) as amount 
    FROM
        evenflow_agg_invoices
    WHERE
        invoice_date >= '{startDate}' and invoice_date <= '{endDate}' 
    GROUP BY
        invoice_date
    ORDER BY 
        invoice_date 
    DESC
"""

INVOICE_TREND_CHART_MONTHLY_QUERY = """
    SELECT 
        TO_CHAR(DATE_TRUNC('month', invoice_date), 'Mon, YYYY') AS month, sum(raised_invoice) as no_of_invoices, sum(raised_invoice_amount) as amount 
    FROM 
        evenflow_agg_invoices
    WHERE 
        DATE_TRUNC('month', invoice_date) >= DATE_TRUNC('month', '{startDate}'::DATE) 
        AND DATE_TRUNC('month', invoice_date) <= DATE_TRUNC('month', '{endDate}'::DATE)
    GROUP BY 
        DATE_TRUNC('month', invoice_date)
    ORDER BY 
        DATE_TRUNC('month', invoice_date) DESC;
"""

INVOICE_TREND_CHART_QUARTERLY_QUERY = """
    SELECT 
        'Q' || CASE
                  WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN 4
                  WHEN EXTRACT(MONTH FROM invoice_date) IN (4, 5, 6) THEN 1
                  WHEN EXTRACT(MONTH FROM invoice_date) IN (7, 8, 9) THEN 2
                  WHEN EXTRACT(MONTH FROM invoice_date) IN (10, 11, 12) THEN 3
              END || ', ' || CASE
                              WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM invoice_date) - 1
                              ELSE EXTRACT(YEAR FROM invoice_date)
                          END AS quarter,
        sum(raised_invoice) as no_of_invoices, sum(raised_invoice_amount) as amount 
    FROM 
        evenflow_agg_invoices
    WHERE 
        invoice_date >= '{startDate}'::DATE 
        AND invoice_date <= '{endDate}'::DATE
    GROUP BY 
        CASE
            WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN 4
            WHEN EXTRACT(MONTH FROM invoice_date) IN (4, 5, 6) THEN 1
            WHEN EXTRACT(MONTH FROM invoice_date) IN (7, 8, 9) THEN 2
            WHEN EXTRACT(MONTH FROM invoice_date) IN (10, 11, 12) THEN 3
        END,
        CASE
            WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM invoice_date) - 1
            ELSE EXTRACT(YEAR FROM invoice_date)
        END
    ORDER BY 
        CASE
            WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN EXTRACT(YEAR FROM invoice_date) - 1
            ELSE EXTRACT(YEAR FROM invoice_date)
        END DESC,
        CASE
            WHEN EXTRACT(MONTH FROM invoice_date) IN (1, 2, 3) THEN 4
            WHEN EXTRACT(MONTH FROM invoice_date) IN (4, 5, 6) THEN 1
            WHEN EXTRACT(MONTH FROM invoice_date) IN (7, 8, 9) THEN 2
            WHEN EXTRACT(MONTH FROM invoice_date) IN (10, 11, 12) THEN 3
        END DESC;

"""

INVOICE_TREND_CHART_YEARLY_QUERY = """
    SELECT 
        TO_CHAR(DATE_TRUNC('year', invoice_date), 'YYYY') AS year, 
        sum(raised_invoice) as no_of_invoices, sum(raised_invoice_amount) as amount 
    FROM 
        evenflow_agg_invoices
    WHERE 
        DATE_TRUNC('year', invoice_date) >= DATE_TRUNC('year', '{startDate}'::DATE) 
        AND DATE_TRUNC('year', invoice_date) <= DATE_TRUNC('year', '{endDate}'::DATE)
    GROUP BY 
        DATE_TRUNC('year', invoice_date)
    ORDER BY 
        DATE_TRUNC('year', invoice_date) DESC;

"""