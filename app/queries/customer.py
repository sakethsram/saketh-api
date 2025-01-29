GET_CUSTOMER_DETAILS = """
    SELECT
	    customer_name, gst_identification_number, gst_treatment, tax_name,
        tax_percentage, payment_terms, payment_terms_label
    FROM 
	    evenflow_customer_master 
    WHERE 
	    id = '{customer_id}' and 
        active_flag = 1
"""

GET_CUSTOMER_ID_USING_CUSTOMER_NAME = """
    SELECT
        id
    FROM
        evenflow_customer_master
    WHERE 
        customer_name = '{customer_name}'
"""