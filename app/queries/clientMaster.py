GET_CLIENT_DETAILS = """
    SELECT
	    bank_name, bank_account_number, ifsc, account_type
    FROM 
	    client_master 
    WHERE 
	    id = '{client_id}' and 
        active_flag = 1
"""