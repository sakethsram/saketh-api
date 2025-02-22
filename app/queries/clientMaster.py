GET_CLIENT_DETAILS = """
    SELECT
	    bank_name, bank_account_number, ifsc, account_type,
        name,pan,gst,client_reg_address_line_1,
        client_reg_address_line_2,client_reg_city,client_reg_state,client_reg_country
    FROM 
	    client_master 
    WHERE 
	    id = '{client_id}' and 
        active_flag = 1
"""