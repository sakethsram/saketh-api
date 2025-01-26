FETCH_PO_LISTING_QUERY = """
        SELECT * FROM(		
		    SELECT 
                EPO.po_processing_status AS type, 
                EPO.po_number, 
                ECM.customer_name,
                EII.appointment_id, 
                EII.appointment_date,
                EPO.accepted_qty AS accepted_quantity,
                EII.place_of_supply,
                EII.created_on AS invoice_input_provided_on,
                EII.invoice_number, 
                EII.invoice_date, 
                EII.invoice_inputs_file_path, 
                EI.invoice_file_path,
                EPO.created_on AS po_created
            FROM 
                evenflow_invoice_inputs AS EII
            JOIN 
                evenflow_purchase_orders AS EPO
            ON 
                EII.evenflow_purchase_orders_id = EPO.id 
                AND 
                EII.client_id = EPO.client_id
                AND 
                EII.active_flag = 1 
                AND 
                EPO.active_flag = 1
            JOIN 
                evenflow_customer_master AS ECM
            ON	
                EPO.evenflow_customer_master_id = ECM.id
                AND 
                ECM.active_flag = 1
            LEFT JOIN
                evenflow_invoices AS EI
            ON
                EI.invoice_number = EII.invoice_number
                AND 
                EI.active_flag = 1

            UNION

            SELECT 
	            EPO.po_processing_status as type, 
	            EPO.po_number, 
	            ECM.customer_name,
	            null as appointment_id, 
	            null as appointment_date, 
	            EPO.accepted_qty as accepted_quantity,
	            null as place_of_supply, 
	            null as invoice_Input_provided_on,
	            null as invoice_number, 
	            null as invoice_date, 
	            null as invoice_inputs_file_path, 
	            null as invoice_file_path,
	            EPO.created_on as po_created
            FROM 
            	evenflow_purchase_orders EPO
            JOIN 
                evenflow_customer_master ECM
            ON	
            	EPO.evenflow_customer_master_id = ECM.id
                AND 
                EPO.active_flag = 1 
                AND 
                ECM.active_flag = 1
            WHERE 
            	EPO.po_processing_status = 'OPEN' 
        ) AS RESULT {whereCondition} ORDER BY RESULT.po_created desc 
        LIMIT {page_size} OFFSET {page_size} * ({page_number} - 1);
    """

FETCH_TOTAL_COUNT_PO_LISTING_QUERY = """
    SELECT count(*) as totalRecords FROM(		
		    SELECT 
                EPO.po_processing_status AS type, 
                EPO.po_number, 
                ECM.customer_name,
                EII.appointment_id, 
                EII.appointment_date,
                EPO.accepted_qty AS accepted_quantity,
                EII.place_of_supply,
                EII.created_on AS invoice_input_provided_on,
                EII.invoice_number, 
                EII.invoice_date, 
                EII.invoice_inputs_file_path, 
                EI.invoice_file_path,
                EPO.created_on AS po_created
            FROM 
                evenflow_invoice_inputs AS EII
            JOIN 
                evenflow_purchase_orders AS EPO
            ON 
                EII.evenflow_purchase_orders_id = EPO.id 
                AND 
                EII.client_id = EPO.client_id
                AND 
                EII.active_flag = 1 
                AND 
                EPO.active_flag = 1
            JOIN 
                evenflow_customer_master AS ECM
            ON	
                EPO.evenflow_customer_master_id = ECM.id
                AND 
                ECM.active_flag = 1
            LEFT JOIN
                evenflow_invoices AS EI
            ON
                EI.invoice_number = EII.invoice_number
                AND 
                EI.active_flag = 1

            UNION

            SELECT 
	            EPO.po_processing_status as type, 
	            EPO.po_number, 
	            ECM.customer_name,
	            null as appointment_id, 
	            null as appointment_date, 
	            EPO.accepted_qty as accepted_quantity,
	            null as place_of_supply, 
	            null as invoice_Input_provided_on,
	            null as invoice_number, 
	            null as invoice_date, 
	            null as invoice_inputs_file_path, 
	            null as invoice_file_path,
	            EPO.created_on as po_created
            FROM 
            	evenflow_purchase_orders EPO
            JOIN 
                evenflow_customer_master ECM
            ON	
            	EPO.evenflow_customer_master_id = ECM.id
                AND 
                EPO.active_flag = 1 
                AND 
                ECM.active_flag = 1
            WHERE 
            	EPO.po_processing_status = 'OPEN' 
        ) AS RESULT {whereCondition}
    """

PO_DETAILS_QUERY_BY_PO_NUMBER = """
    SELECT  
	    po_status,
	    vendor,
	    ship_to_location,
	    ordered_on,
	    ship_window_from,
	    freight_terms,
	    payment_method,
	    payment_terms,
	    purchasing_entity,
	    submitted_items,
	    submitted_qty,
        submitted_total_cost,
        accepted_items,
        accepted_qty,
        accepted_total_cost,
        received_items,
        received_qty,
        received_total_cost,
	    cancelled_items,
        cancelled_qty,
        cancelled_total_cost,
	    delivery_address
    FROM
	    evenflow_purchase_orders 
    WHERE 
        po_number = '{po_number}'
    """
PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITHOUT_FULFILLED = """
    SELECT
	    asin,
	    external_id,
	    model_number,
	    hsn,
	    title,
	    window_type,
	    expected_date,
	    qty_requested,
	    qty_accepted,
	    qty_received,
	    qty_outstanding,
	    unit_cost,
	    total_cost
    FROM 
	    evenflow_purchase_orders_line_items poli
    JOIN 
	    evenflow_purchase_orders po
    ON 
	    po.id = poli.evenflow_purchase_orders_id
    WHERE 
	    po.po_number = '{po_number}' and
        poli.po_line_item_processing_status != 'FULFILLED'

    """

PO_LINE_ITEM_DETAILS_QUERY_BY_PO_NUMBER_WITH_FULFILLED = """
    SELECT
	    asin,
	    external_id,
	    model_number,
	    hsn,
	    title,
	    window_type,
	    expected_date,
	    qty_requested,
	    qty_accepted,
	    qty_received,
	    qty_outstanding,
	    unit_cost,
	    total_cost
    FROM 
	    evenflow_purchase_orders_line_items poli
    JOIN 
	    evenflow_purchase_orders po
    ON 
	    po.id = poli.evenflow_purchase_orders_id
    WHERE 
	    po.po_number = '{po_number}'

    """
