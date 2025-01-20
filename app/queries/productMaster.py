GET_PRODUCT_DETAILS = """
    SELECT 
        id, item_name, hsn_sac, taxable as is_inclusive_tax, account, description, product_type,
        usage_unit, rate, exemption_reason, intra_state_tax_name, intra_state_tax_type, intra_state_tax_rate
    FROM 
        evenflow_product_master
    WHERE 
        sku = '{sku}'
"""