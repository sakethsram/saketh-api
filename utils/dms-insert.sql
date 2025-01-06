--SET search_path TO platform;

INSERT INTO screens
(screen_id, screen_name, screen_description, created_on, created_by, modified_on, modified_by, active_flag)
VALUES( 1, 'CLIENT_ONBOARDING_INVOICE_GENERATION_MAIN_SCREEN', 'Screen used by Admin to capture disty & accounting details', CURRENT_TIMESTAMP,'prakash.n@samyudhi.com' , CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 2, 'CLIENT_ONBOARDING_INVOICE_GENERATION_PO_SCREEN', 'Screen used by Admin to upload sample PO file and confirm field mappings', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 3, 'CLIENT_ONBOARDING_INVOICE_GENERATION_ITEM_MASTER_SCREEN', 'Screen used by Admin to upload latest Item Master file and confirm field mappings', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 4, 'CLIENT_ONBOARDING_INVOICE_GENERATION_CUSTOMER_MASTER_SCREEN', 'Screen used by Admin to upload latest Customer Master file and confirm field mappings', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 5, 'PO_DASHBOARD_SCREEN', 'Screen used by Category Managers to view PO dashboard', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 6, 'PO_LISTING_SCREEN', 'Screen used by Category Managers to view list of POs', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 7, 'INVOICE_INPUTS_GENERATION_SCREEN', 'Screen used by Category Managers to create Invoice Inputs', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 8, 'INVOICE_DASHBOARD_SCREEN', 'Screen used by FinOps to view Invoice dashboard', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 9, 'INVOICE_LISTING_SCREEN', 'Screen used by FinOps to view list of Invoices', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 10, 'INVOICE_GENERATION_SCREEN', 'Screen used by FinOps to view generate Invoices', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 11, 'INVOICE_PAYMENTS_SCREEN', 'Screen used by FinOps to view Invoice payments', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
( 12, 'INVOICE_EWAYBILL_SCREEN', 'Screen used by FinOps to generate e-Waybill for an Invoice', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);


INSERT INTO client_master
(id, "name", pan, gst, client_reg_address_line_1, client_reg_address_line_2, 
client_reg_city, client_reg_state, client_reg_country, created_on, created_by, modified_on, modified_by, active_flag,url)
VALUES(nextval('client_master_id_seq'::regclass), 'Evenflow', 'QWERT3451G', '27AAAPA1234A1Z5', 
'3rd floor, Evenflow Brands', '2732, 27th Main Rd, Sector 2, PWD Quarters, 1st Sector',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1,'https://www.evenflowbrands.com'),
(nextval('client_master_id_seq'::regclass), 'DataWorkx', 'SAMTE3331C', '12AAAPA1234A1Z4', 
'39, JR Greenwich Layout', 'Off Sarjapur Road, Kodathi',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0,'https://dataworkx.ai/');


INSERT INTO disty_master
(id, "name", pan, gst, registered_address_line_1, registered_address_line_2, registered_city, registered_state, registered_country, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('disty_master_id_seq'::regclass), 'Retail EZ', '', '', 'Plot No. 12 P2', 
'Hitech, Defence and Aerospace Park, Devanahalli', 'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('client_master_id_seq'::regclass), 'ETrade', '', '', 
'', '',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('client_master_id_seq'::regclass), 'CickTech', '', '', 
'', '',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('client_master_id_seq'::regclass), 'RK World', '', '', 
'', '',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('client_master_id_seq'::regclass), 'CocoBlue', '', '', 
'', '',
'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1)
;



INSERT INTO platform_features_master
(id, feature, monthly_license_fees, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('platform_features_master_id_seq'::regclass), 'INVOICE_GENERATION_B2B', 100000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('platform_features_master_id_seq'::regclass), 'MARKETPLACE_REPORTS_DOWNLOAD', 120000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('platform_features_master_id_seq'::regclass), 'INVOICE_GENERATION_B2C', 110000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('platform_features_master_id_seq'::regclass), 'MARKETPLACE_P&L_STATEMENT', 100000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('platform_features_master_id_seq'::regclass), 'CASHFLOW_STATEMENT', 100000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('platform_features_master_id_seq'::regclass), 'GST/TAX_STATEMENT', 100000.00, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0);


INSERT INTO market_place_master   --recomondation we can add url
(id, marketplace_name, created_on, created_by, modified_on, modified_by, active_flag)
VALUES
(nextval('market_place_master_id_seq'::regclass), 'Amazon B2B', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Amazon B2C', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Flipkart B2B', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Flipkart B2C', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Zepto', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Myntra', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Nykaa', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Ajio', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'BigBasket', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Swiggy', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Zomato', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Reliance Digital', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Lenskart', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Tata CliQ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'CRED', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Blinkit', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Shopify', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Meesho', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'FirstCry', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Snapdeal', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Paytm Mall', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Pepperfry', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('market_place_master_id_seq'::regclass), 'Urban Ladder', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);



/*PRAKASH TO RECREATE & RELOAD THIS TABLE AS PER THE LATEST CUSTOMER MASTER FILE*/
--TRUNCATE TABLE evenflow_customer_master RESTART IDENTITY CASCADE;
INSERT INTO evenflow_customer_master
(
    id, 
    client_id, 
    customer_name, 
    customer_contact_salutation, 
    customer_contact_first_name, 
    customer_contact_last_name, 
    customer_contact_phone, 
    currency_code, 
    website, 
    opening_balance, 
    opening_balance_exchange_rate, 
    bank_account_payment, 
    credit_limit, 
    customer_sub_type, 
    billing_attention, 
    billing_address_line_1, 
    billing_address_line_2, 
    billing_city, 
    billing_state, 
    billing_country, 
    billing_code, 
    billing_phone, 
    billing_fax, 
    shipping_attention, 
    shipping_address_line_1, 
    shipping_address_line_2, 
    shipping_city, 
    shipping_state, 
    shipping_country, 
    shipping_code, 
    shipping_phone, 
    shipping_fax, 
    skype_handle, 
    facebook_handle,
    twitter_handle, 
    department, 
    designation, 
    price_list, 
    payment_terms, 
    payment_terms_label, 
    gst_treatment, 
    gst_identification_number, 
    owner_name, 
    primary_contact_id, 
    email_id, 
    mobile_phone, 
    contact_id, 
    contact_name, 
    contact_type, 
    place_of_contact, 
    place_of_contact_with_state_code, 
    taxable, 
    tax_id, 
    tax_name, 
    tax_percentage, 
    exemption_reason, 
    contact_address_id, 
    created_on, 
    created_by, 
    modified_on, 
    modified_by, 
    active_flag,
    --company_name,
    sales_channel, branch_id,branch_name,cf_msme
    --,portal_enabled

)     
SELECT 
    nextval('evenflow_customer_master_id_seq'::regclass), 
    1 as client_id, 
    display_name as customer_name, 
    salutation as customer_contact_salutation, 
    first_name as customer_contact_first_name, 
    last_name as customer_contact_last_name, 
    phone as customer_contact_phone, 
    currency_code, 
    website, 
    CAST(NULLIF(opening_balance,'') AS numeric(20, 2)) as opening_balance, 
    CAST(NULLIF(opening_balance_exchange_rate,'') AS numeric(20, 2)) as opening_balance_exchange_rate, 
     CASE 
        WHEN bank_account_payment = 'TRUE' THEN 1 
        ELSE  0
    END as bank_account_payment, 
    CAST(NULLIF(credit_limit,'') AS numeric(20, 2)) as credit_limit, 
    customer_sub_type, 
    billing_attention, 
    billing_address as billing_address_line_1, 
    billing_street2 as billing_address_line_2, 
    billing_city, 
    billing_state, 
    billing_country, 
    billing_code, 
    billing_phone, 
    billing_fax, 
    shipping_attention, 
    shipping_address as shipping_address_line_1, 
    shipping_street2 as shipping_address_line_2, 
    shipping_city, 
    shipping_state, 
    shipping_country, 
    shipping_code, 
    shipping_phone, 
    shipping_fax, 
    skype_identity as skype_handle, 
    facebook as facebook_handle, 
    twitter as twitter_handle, 
    department, 
    designation, 
    price_list, 
    payment_terms, 
    payment_terms_label, 
    gst_treatment, 
    gst_identification_number_gstin, 
    owner_name, 
    primary_contact_id, 
    emailid, 
    mobilephone, 
    contact_id, 
    contact_name, 
    contact_type, 
    place_of_contact, 
    place_of_contact_with_state_code, 
      CASE 
        WHEN taxable = 'TRUE' THEN 1 
        ELSE 0
    END as taxable,
    taxid, 
    tax_name, 
    CAST(nullif(tax_percentage,'') AS numeric(20, 2)) as tax_percentage, 
    exemption_reason, 
    cast(contact_address_id as float4) as contact_address_id, 
    CURRENT_TIMESTAMP as created_on, 
    'prakash.n@samyudhi.com' as created_by, 
    CURRENT_TIMESTAMP as modified_on, 
    'prakash.n@samyudhi.com' as modified_by, 
    1 as active_flag,
    --company_name,
    sales_channel, 
    cast(NULLIF(branch_id,'') as int8) as branch_id, -- CAST(NULLIF("Reorder Point", '') AS numeric(20, 2)) as reorder_point,
    branch_name,
    cf_msme    
--      CASE 
--        WHEN portal_enabled = 'false' THEN 0 
--        ELSE 1
--    END as portal_enabled
FROM stage_tables.customers_zoho_master;



/*PRAKASH TO RECREATE & RELOAD THIS TABLE AS PER THE LATEST PRODUCT MASTER FILE*/
INSERT INTO evenflow_product_master
( client_id, item_id, item_name, sku, hsn_sac
, description, rate, 
    account, account_code, taxable
    , exemption_reason, taxability_type, product_type, intra_state_tax_name, intra_state_tax_rate, 
    intra_state_tax_type, inter_state_tax_name, inter_state_tax_rate, inter_state_tax_type, usage_unit, purchase_rate,
    purchase_account, purchase_account_code, purchase_description, inventory_account, inventory_account_code, reorder_point, 
    vendor, opening_stock, opening_stock_value, stock_on_hand, item_type, 
cf_asin, created_on, created_by, modified_on, modified_by, active_flag,
parent_category, warehouse_name, is_combo_product, brand, sales_channel, 
cf_fsn, cf_old_sku, cf_old_asin, cf_old_fsn, cf_box_count, cf_myntra_style_id, 
cf_az_tp_excl_gst, cf_mrp_with_tax, 
cf_fk_tp_excl_gst, cf_instamart_tp_excl_gst, cf_ean, 
cf_brands, cf_blinkit_id, cf_blinkit_tp,
"source", reference_id, status 
)
SELECT 
    1 as client_id, 
    CAST(Item_ID as float4) as item_id,                         
    Item_Name as item_name,                                                   
    sku as sku,                                                              
   COALESCE(
    CASE 
      WHEN hsn_sac ~ '^[0-9]+$' THEN CAST(hsn_sac AS int4)  
      ELSE NULL  
    END, 
    0  
  ) AS hsn_sac,                                           
    Description as description,                                               
    CAST(regexp_replace(Rate, '[^0-9.]+', '', 'g') AS numeric(20, 2)) as rate,                                     
    Account as account,                                                       
    Account_Code as account_code, 
     CASE 
        WHEN Taxable = 'false' THEN 0 
        ELSE 1
    END as Taxable,                                       
    exemption_reason as exemption_reason,                                  
    taxability_type as taxability_type,                                       
    product_type as product_type,                                             
    intra_state_tax_name as intra_state_tax_name,                             
    CAST(NULLIF(intra_state_tax_rate,'') as numeric(20, 2)) as intra_state_tax_rate,     
    intra_state_tax_type as intra_state_tax_type,                             
    intra_state_tax_type as inter_state_tax_name,                             
    CAST(NULLIF(inter_state_tax_rate,'') as numeric(20, 2)) as inter_state_tax_rate,     
    inter_state_tax_type as inter_state_tax_type,                             
    usage_unit as usage_unit,
    CAST(regexp_replace(NULLIF(purchase_rate,''), '[^0-9.]+', '', 'g') AS numeric(20, 2)) as purchase_rate, 
    purchase_account as purchase_account,                                     
    purchase_account_code as purchase_account_code,                           
    purchase_description as purchase_description,                             
    inventory_account as inventory_account,                                   
    inventory_account_code as inventory_account_code,                         
    CAST(NULLIF(reorder_point, '') AS numeric(20, 2)) as reorder_point,                   
    vendor as vendor,                                                        
    CAST(NULLIF(opening_stock, '') AS numeric(20, 2)) as opening_stock, --  CAST(NULLIF(regexp_replace(opening_stock_value, '[^0-9.]+', '', 'g'), '') AS numeric(20, 2))
	CAST(NULLIF(regexp_replace(opening_stock_value, '[^0-9.]+', '', 'g'), '') AS numeric(20, 2)) as opening_stock_value,
	null as stock_on_hand,                 
    item_type as item_type,                                                   
    cf_asin as cf_asin,                                                       
    CURRENT_TIMESTAMP as created_on, 
    'prakash.n@samyudhi.com' as created_by, 
    CURRENT_TIMESTAMP as modified_on, 
    'prakash.n@samyudhi.com' as modified_by, 
    1 as active_flag,
    parent_category, warehouse_name,
     CASE 
        WHEN is_combo_product = 'false' THEN 0 
        ELSE 1
    END as is_combo_product,
    brand, sales_channel, 
cf_fsn, cf_old_sku, cf_old_asin, cf_old_fsn, cast(NULLIF(cf_box_count,'') as int) as cf_box_count, cf_myntra_style_id, 
cast(NULLIF("cf_az_tp(ex-GST)",'')as numeric) as "cf_az_tp(ex-GST)", cast(NULLIF("cf_mrp(w tax)",'') as numeric) as "cf_mrp(w tax)", 
 cast(NULLIF("cf_fk_tp (ex-GST)",'') as numeric) as "cf_fk_tp (ex-GST)", cast(NULLIF("cf_instamart_tp (ex-GST)",'') as numeric) as "cf_instamart_tp (ex-GST)", cf_ean, 
cf_brands, cf_blinkit_id, cast(NULLIF(cf_blinkit_tp,'') as numeric) as cf_blinkit_tp,
"source", reference_id, status 
FROM stage_tables.item_zoho_master;


INSERT INTO evenflow_warehouses
(id, client_id, warehouse_id, warehouse_name, warehouse_address_line_1, warehouse_address_line_2, 
warehouse_city, warehouse_state, warehouse_country, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('evenflow_warehouses_id_seq'::regclass), 1, '1001', 'Navdurga Logistics Yeshwanthpur', 'B 107, 3RD CROSS', 
'2ND STAGE, DDUTTL', 'Yeshwanthpur', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('evenflow_warehouses_id_seq'::regclass), 1, '1002', 'Evenflow Blr Warehouse', 'Plot No.68, It Park', 
'Number 8, Kiadb', 'Bengaluru', 'Karnataka', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('evenflow_warehouses_id_seq'::regclass), 1, '1003', 'Evenflow MUMBAI  Warehouse', 'FLAT NO 201,PLOT NO. 148,ODYSSEY', 
'RAHEJA REFLECTION PHASE-II,NEAR GOKUL CONCORDE ', 'MUMBAI', 'Maharashtra', 'INDIA', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);


INSERT INTO evenflow_market_place_details
(id, client_id, market_place_master_id, market_place_url, market_place_userid, market_place_pwd, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('evenflow_market_place_details_id_seq'::regclass), 1, 1, 'https://sell.amazon.in/sell-online', 'Evenflow_Admin_User', 'EvenflowAmazon@2025', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('evenflow_market_place_details_id_seq'::regclass), 1, 2, 'https://www.flipkart.com/b2b-online-marketing', 'Evenflow_Admin_User', 'EvenflowFlipkart@2025', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('evenflow_market_place_details_id_seq'::regclass), 1, 17, 'https://www.firstcry.com/sell-online', 'Evenflow_Admin_User', 'EvenflowFirstCry@2025', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);

INSERT INTO client_subscriptions
(id, client_id, feature_id, monthly_license_fees, subscription_end_date, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('client_subscriptions_id_seq'::regclass), 1, 1, 100000.00, CURRENT_TIMESTAMP + INTERVAL '1 month',CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('client_subscriptions_id_seq'::regclass), 1, 2, 120000.00,CURRENT_TIMESTAMP + INTERVAL '1 month', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('client_subscriptions_id_seq'::regclass), 1, 3, 110000.00,CURRENT_TIMESTAMP + INTERVAL '1 month', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('client_subscriptions_id_seq'::regclass), 1, 4, 100000.00,CURRENT_TIMESTAMP + INTERVAL '1 month', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('client_subscriptions_id_seq'::regclass), 1, 5, 100000.00,CURRENT_TIMESTAMP + INTERVAL '1 month', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0),
(nextval('client_subscriptions_id_seq'::regclass), 1, 6, 100000.00,CURRENT_TIMESTAMP + INTERVAL '1 month', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 0);


/*INSERT INTO evenflow_accounting_details
(id, client_id, invoice_inputs, invoice_number_auto, accounting_tool_name, accounting_tool_url, accounting_tool_userid, accounting_tool_pwd, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('evenflow_accounting_details_id_seq'::regclass), 1, 'PO', 0, 'ZohoBooks', 'https://books.zoho.in', 'ZohoAdminUser', 'Password@143', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);*/


INSERT INTO roles
(id, role_name, role_description, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('roles_id_seq'::regclass), 'ADMIN', '', CURRENT_TIMESTAMP,'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_id_seq'::regclass), 'CATEGORYMANAGER', '', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_id_seq'::regclass), 'FINOPS', '', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);


INSERT INTO users
(id, user_first_name, user_last_name, user_e_mail_id, user_phone_number, user_login_id, user_password, client_id, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('users_id_seq'::regclass), 'Prakash', 'Naidu', 'prakash.n@samyudhi.com', '9701123456', 'prakash.n@samyudhi.com', 
'Password@123', 2, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'Utsav', 'Agarwal', 'Utsav.a@evenflow.com', '9701123456', 'Utsav.a@evenflow.com', 
'Password@123', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'bhagavan', 'prasad', 'bhagavansprasad@gmail.com', '9700983456', 'bhagavansprasad@gmail.com', 
'PrasadB@2025', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'ikshwa', 'kv', 'ikshwakv@gmail.com', '7891123456', 'ikshwakv@gmail.com', 
'IkshwaKV@123', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'dasharadha', 'ram', 'dasharadharam70@gmail.com', '6301123456', 'dasharadharam70@gmail.com', 
'RamD@2025', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'likhita', 'beekam', 'likhitabeekam@gmail.com', '9701654456', 'likhitabeekam@gmail.com', 
'LikhitaB@123', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'sai', 'nath', 'sainathvitp@gmail.com', '9745611231', 'sainathvitp@gmail.com', 
'SainathVIT@123', 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('users_id_seq'::regclass), 'Sudhakar', 'KSS', 'sudhakar.kss@dataworkx.ai', '9708176456', 'sudhakar.kss@dataworkx.ai', 
'SudhakarKSS@123', 2, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);


INSERT INTO user_roles
(id, user_id, role_id, created_on, created_by, modified_on, modified_by, active_flag)
VALUES(nextval('user_roles_id_seq'::regclass), 1, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 8, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 2, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 3, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 4, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 5, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 6, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('user_roles_id_seq'::regclass), 7, 3, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);



INSERT INTO feature_privileges
(id, screen_id, privilege_type, created_on, created_by, modified_on, modified_by, active_flag)
VALUES
(nextval('feature_privileges_id_seq'::regclass), 1, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 2, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 3, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 4, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 5, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 6, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 7, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 8, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 9, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 10, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 11, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 12, 'SAVE', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 1, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 2, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 3, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 4, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 5, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 6, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 7, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 8, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 9, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 10, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 11, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('feature_privileges_id_seq'::regclass), 12, 'READ', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);


INSERT INTO roles_feature_privileges
(id, screen_id, role_id, feature_privileges_id, privilege_access, created_on, created_by, modified_on, modified_by, active_flag)
VALUES
(nextval('roles_feature_privileges_id_seq'::regclass), 1, 1, 1, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 1, 2, 1, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 1, 3, 1, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 2, 1, 2, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 2, 2, 2, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 2, 3, 2, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 3, 1, 3, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 3, 2, 3, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 3, 3, 3, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 4, 1, 4, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 4, 2, 4, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 4, 3, 4, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 5, 1, 5, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 5, 2, 5, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 5, 3, 5, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 6, 1, 6, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 6, 2, 6, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 6, 3, 6, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 7, 1, 7, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 7, 2, 7, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 7, 3, 7, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 8, 1, 8, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 8, 2, 8, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 8, 3, 8, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 9, 1, 9, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 9, 2, 9, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 9, 3, 9, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 10, 1, 10, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 10, 2, 10, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 10, 3, 10, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 11, 1, 11, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 11, 2, 11, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 11, 3, 11, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 12, 1, 12, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 12, 2, 12, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1),
(nextval('roles_feature_privileges_id_seq'::regclass), 12, 3, 12, 1, CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', CURRENT_TIMESTAMP, 'prakash.n@samyudhi.com', 1);



-----------------------------------------------------------------------------------------
/*
select * from screens --
select * from disty_master --
select * from client_master --
select * from platform_features_master --
select * from client_subscriptions --
select * from roles --
select * from users --
select * from user_roles --
select * from feature_privileges --
select * from roles_feature_privileges --
select * from market_place_master  --
select * from evenflow_customer_master --
select * from evenflow_product_master  --
select * from evenflow_warehouses --
select * from evenflow_market_place_details --
*/

/*
evenflow_agg_po_invoices
evenflow_invoice_inputs
evenflow_invoice_payments
evenflow_invoices
evenflow_purchase_orders
evenflow_purchase_orders_line_items
evenflow_accounting_details --
*/




