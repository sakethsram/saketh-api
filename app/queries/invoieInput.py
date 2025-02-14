CREATE_INVOICE_INPUT = """
    INSERT INTO 
        evenflow_invoice_inputs (
	        client_id, evenflow_customer_master_id, evenflow_product_master_id, invoice_status, 
            customer_name, gst_treatment, tcs_tax_name, tcs_percentage, 
            gstin, place_of_supply, purchase_order_number, evenflow_purchase_orders_line_items_id, evenflow_purchase_orders_id,  
            payment_terms, payment_terms_label, expected_date, account, 
            item_name, sku, item_desc, item_type, 
            hsn_sac, quantity, usage_unit, item_price, 
            item_tax_exemption_reason, is_inclusive_tax, item_tax, item_tax_type, 
            item_tax_percentage, notes,  fiscal_quarter, po_month, 
            po_year, appointment_id, appointment_date, accepted_qty, 
            invoice_generated_acc_tool, po_file_path,  box_number, total_box_count, 
            active_flag, created_by, other_warehouse_name, other_warehouse_address_line_1,
            other_warehouse_address_line_2, other_warehouse_city, other_warehouse_state, other_warehouse_country,
            other_warehouse_postal_code, modified_by, iteration_id

	    )
	    VALUES (
		    :clientId, :evenflowCustomerMasterId, :evenflowProductMasterId, :invoiceStatus,
		    :customerName, :gstTreatment, :tcsTaxName, :tcsPercentage, 
            :gstin, :placeOfSupply, :poNumber, :poLineItemId, :evenflowPurchaseOrdersId,
		    :paymentTerms, :paymentTermsLabel, :expectedDate, :account, 
            :itemName, :sku, :itemDesc, :itemType,
		    :hsnSac, :quantity, :usageUnit, :itemPrice,
		    :itemTaxExemptionReason, :isInclusiveTax, :itemTax, :itemTaxType,
            :itemTaxPercentage, :notes, :fiscalQuarter, :poMonth, 
            :poYear, :appointmentId, :appointmentDate, :acceptedQty, 
            :invoiceGeneratedAccTool, :poFilePath, :boxNumber, :totalBoxCount, 
            :activeFlag, :createdBy, :otherWarehouseName, :otherWarehouseAddressLine1,
            :otherWarehouseAddressLine2, :otherWarehouseCity, :otherWarehouseState, :otherWarehouseCountry,
            :otherWarehousePostalCode, :modifiedBy, :iterationNumber
	)
"""


GET_MAX_ITERATION_NUMBER = """
    SELECT 
        max(iteration_id) as iteration_id
    FROM
        evenflow_invoice_inputs
    WHERE
        purchase_order_number = '{poNumber}' AND
        active_flag = 1
"""

UPDATE_PROCESSING_STATUS = """
    WITH LatestInvoiceInput AS (
        SELECT
            ei.evenflow_purchase_orders_line_items_id,
            ei.id AS invoice_input_id,
            ROW_NUMBER() OVER (PARTITION BY ei.evenflow_purchase_orders_line_items_id 
	    	ORDER BY ei.id DESC) AS rn
        FROM evenflow_invoice_inputs ei
        WHERE ei.evenflow_purchase_orders_line_items_id = {poLineItemId}
    )
    UPDATE evenflow_invoice_inputs ei
    SET po_line_item_processing_status = CASE
        WHEN poi.po_line_item_processing_status = 'FULFILLED' THEN 'FULFILLED'
        ELSE 'PARTIALLY_FULFILLED'
    END
    FROM LatestInvoiceInput li
    JOIN evenflow_purchase_orders_line_items poi
        ON poi.id = li.evenflow_purchase_orders_line_items_id
    WHERE ei.id = li.invoice_input_id
      AND li.rn = 1; 
"""