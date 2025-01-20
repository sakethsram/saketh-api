GET_ACCOUNTING_DETAILS = """
    SELECT 
        id as accounting_tool_id
    FROM 
        evenflow_accounting_details
    WHERE
        client_id = '{client_id}'
"""