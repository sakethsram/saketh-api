GET_WAREHOUSE_DETAILS = """
    SELECT 
        warehouse_id, warehouse_name
    FROM
        evenflow_warehouses
    WHERE
        active_flag = 1
"""