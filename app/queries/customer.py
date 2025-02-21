GET_CUSTOMER_DETAILS = """
    SELECT
	    customer_name, gst_identification_number, gst_treatment, tax_name,
        tax_percentage, payment_terms, payment_terms_label, billing_attention ,
        billing_address_line_1 , billing_address_line_2 , billing_city , billing_state ,
        billing_country , billing_code , billing_phone , billing_fax ,
        shipping_attention , shipping_address_line_1 , shipping_address_line_2 , shipping_city ,
        shipping_state , shipping_country , shipping_code , shipping_phone ,
        shipping_fax
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