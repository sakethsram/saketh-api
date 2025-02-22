CREATE_INVOICE_INPUT = """
    INSERT INTO 
        evenflow_invoice_inputs (
	        client_id, evenflow_customer_master_id, evenflow_product_master_id, invoice_status, 
            customer_name, gst_treatment, tcs_tax_name, tcs_percentage, 
            gstin, place_of_supply, purchase_order_number, evenflow_purchase_orders_line_items_id, evenflow_purchase_orders_id,  
            payment_terms, payment_terms_label, expected_date, account, 
            item_name, sku, item_desc, item_type, 
            hsn_sac, quantity, usage_unit, item_price, 
            item_tax_exemption_reason, is_inclusive_tax, notes,  fiscal_quarter, po_month, 
            po_year, appointment_id, appointment_date, accepted_qty, 
            invoice_generated_acc_tool, po_file_path,  box_number, total_box_count, 
            active_flag, created_by, other_warehouse_name, other_warehouse_address_line_1,
            other_warehouse_address_line_2, other_warehouse_city, other_warehouse_state, other_warehouse_country,
            other_warehouse_postal_code, modified_by, iteration_id, billing_attention ,
            billing_address_line_1 , billing_address_line_2 , billing_city , billing_state ,
            billing_country , billing_code , billing_phone , billing_fax ,
            shipping_attention , shipping_address_line_1 , shipping_address_line_2 , shipping_city ,
            shipping_state , shipping_country , shipping_code , shipping_phone ,
            shipping_fax , brand_bank_name , brand_bank_account_number , brand_ifsc ,
            brand_bank_account_type,brand_name,brand_pan,brand_gstin,
            brand_reg_address_line_1 ,brand_reg_address_line_2 ,brand_reg_city,	brand_reg_state,
            brand_reg_country
	    )
	    VALUES (
		    :clientId, :evenflowCustomerMasterId, :evenflowProductMasterId, :invoiceStatus,
		    :customerName, :gstTreatment, :tcsTaxName, :tcsPercentage, 
            :gstin, :placeOfSupply, :poNumber, :poLineItemId, :evenflowPurchaseOrdersId,
		    :paymentTerms, :paymentTermsLabel, :expectedDate, :account, 
            :itemName, :sku, :itemDesc, :itemType,
		    :hsnSac, :quantity, :usageUnit, :itemPrice,
		    :itemTaxExemptionReason, :isInclusiveTax, :notes, :fiscalQuarter, :poMonth, 
            :poYear, :appointmentId, :appointmentDate, :acceptedQty, 
            :invoiceGeneratedAccTool, :poFilePath, :boxNumber, :totalBoxCount, 
            :activeFlag, :createdBy, :otherWarehouseName, :otherWarehouseAddressLine1,
            :otherWarehouseAddressLine2, :otherWarehouseCity, :otherWarehouseState, :otherWarehouseCountry,
            :otherWarehousePostalCode, :modifiedBy, :iterationNumber, :billingAttention,   
            :billingAddressLine1, :billingAaddressLine2, :billingCity, :billingState,        
            :billingCountry, :billingCode, :billingPhone, :billingFax,          
            :shippingAttention, :shippingAddressLine1, :shippingAddressLine2, :shippingCity,       
            :shippingState, :shippingCountry, :shippingCode, :shippingPhone,       
            :shippingFax, :bankName, :bankAccountNumber, :ifsc, 
            :accountType, :brandName, :brandPan, :brandGstin,
            :brandRegAddressLine1, :brandRegAddressLine2, :brandRegCity,:brandRegState,
            :brandRegCountry

        )
"""

# item_tax, item_tax_type, 
#             item_tax_percentage, :itemTax, :itemTaxType,
            # :itemTaxPercentage,


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


UPDATE_TAX_COLUMNS = """
WITH LatestInvoiceInput AS (
    SELECT
        ei.evenflow_purchase_orders_line_items_id,
        ei.id AS invoice_input_id,
        ROW_NUMBER() OVER (PARTITION BY ei.evenflow_purchase_orders_line_items_id 
        ORDER BY ei.id DESC) AS rn
    FROM evenflow_invoice_inputs ei
    WHERE ei.evenflow_purchase_orders_line_items_id = {poLineItemId}
),
TaxInputs AS (
    SELECT 
        CASE 
            WHEN c.client_reg_state = cm.shipping_state THEN pm.intra_state_tax_name 
            ELSE pm.inter_state_tax_name 
        END AS tax_name,
        CASE 
            WHEN c.client_reg_state = cm.shipping_state THEN pm.intra_state_tax_type 
            ELSE pm.inter_state_tax_type 
        END AS tax_type,
        CASE 
            WHEN c.client_reg_state = cm.shipping_state THEN pm.intra_state_tax_rate 
            ELSE pm.inter_state_tax_rate 
        END AS tax_rate,
        CASE 
            WHEN c.client_reg_state = cm.shipping_state THEN pm.intra_state_tax_rate / 2 
            ELSE pm.inter_state_tax_rate 
        END AS gst_rate,
        CASE 
            WHEN c.client_reg_state = cm.shipping_state THEN 'intra_state_tax_rate' 
            ELSE 'inter_state_tax_rate' 
        END AS gst_type    
    FROM evenflow_product_master pm
    JOIN client_master c ON pm.client_id = c.id
    JOIN evenflow_customer_master cm ON cm.id = {customer_master_id} AND pm.client_id = cm.client_id
    WHERE pm.id = {product_master_id}
)
UPDATE evenflow_invoice_inputs ei
SET 
    item_tax = ti.tax_name,
    item_tax_type = ti.tax_type,
    item_tax_percentage = ti.tax_rate,
    cgst_percentage = CASE WHEN ti.gst_type = 'intra_state_tax_rate' THEN ti.gst_rate ELSE 0 END,
    sgst_percentage = CASE WHEN ti.gst_type = 'intra_state_tax_rate' THEN ti.gst_rate ELSE 0 END,
    igst_percentage = CASE WHEN ti.gst_type = 'inter_state_tax_rate' THEN ti.gst_rate ELSE 0 END,
    cgst_amount = (ei.quantity * ei.item_price * CASE WHEN ti.gst_type = 'intra_state_tax_rate' THEN ti.gst_rate ELSE 0 END) / 100,
    sgst_amount = (ei.quantity * ei.item_price * CASE WHEN ti.gst_type = 'intra_state_tax_rate' THEN ti.gst_rate ELSE 0 END) / 100,
    igst_amount = (ei.quantity * ei.item_price * CASE WHEN ti.gst_type = 'inter_state_tax_rate' THEN ti.gst_rate ELSE 0 END) / 100,
    amount = ei.quantity * ei.item_price
FROM TaxInputs ti
WHERE ei.evenflow_purchase_orders_line_items_id = {poLineItemId}
AND ei.id IN (SELECT invoice_input_id FROM LatestInvoiceInput WHERE rn = 1);

"""