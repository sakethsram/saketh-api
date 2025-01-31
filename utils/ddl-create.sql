--SET search_path TO platform;

/*Has details of all features offered currently*/
DROP TABLE platform_features_master;
CREATE TABLE platform_features_master (
	id SERIAL PRIMARY KEY,
	feature VARCHAR(125) NOT NULL,
	monthly_license_fees DECIMAL(20,2),
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL
);


/*List of all Clients on-boarded on to the platform*/
DROP TABLE client_master;
CREATE TABLE client_master (
	id SERIAL PRIMARY KEY,
	name VARCHAR(125) NOT NULL,
	pan VARCHAR(125) NOT NULL,
	gst VARCHAR(125) NOT NULL,
	client_reg_address_line_1 VARCHAR(250) NOT NULL,
	client_reg_address_line_2 VARCHAR(250),
	client_reg_city VARCHAR(125) NOT NULL,
	client_reg_state VARCHAR(125) NOT NULL,
	client_reg_country VARCHAR(125) NOT NULL,
	url VARCHAR(125),
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL
);


/*List of all Distributors leveraged by Clients*/
DROP TABLE disty_master;
CREATE TABLE disty_master (
	id SERIAL PRIMARY KEY,
	name VARCHAR(125) NOT NULL,
	pan VARCHAR(125),
	gst VARCHAR(125),
	registered_address_line_1 VARCHAR(250),
	registered_address_line_2 VARCHAR(250),
	registered_city VARCHAR(125),
	registered_state VARCHAR(125),
	registered_country VARCHAR(125),
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL
);

/*Client specific table - List of all Clients' Warehouses*/
DROP TABLE evenflow_warehouses;
CREATE TABLE evenflow_warehouses (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	warehouse_id VARCHAR(125) NOT NULL,
	warehouse_name VARCHAR(125) NOT NULL,
	warehouse_address_line_1 VARCHAR(250) NOT NULL,
	warehouse_address_line_2 VARCHAR(250),
	warehouse_city VARCHAR(125) NOT NULL,
	warehouse_state VARCHAR(125) NOT NULL,
	warehouse_country VARCHAR(125) NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_warehouses_1 FOREIGN KEY (client_id) REFERENCES client_master(id)
);

/*Client specific table - List of all Clients' Distys*/
DROP TABLE evenflow_distys;
CREATE TABLE evenflow_distys (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	disty_id INTEGER NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_distys_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_distys_2 FOREIGN KEY (disty_id) REFERENCES disty_master(id)
);

/*Client specific table - Has details about each Client's customers*/
--DROP TABLE public.evenflow_customer_master CASCADE;
/*PRAKASH TO RECREATE THIS TABLE*/
DROP TABLE evenflow_customer_master;
CREATE TABLE evenflow_customer_master (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	customer_name VARCHAR(125) NOT NULL,
	customer_contact_salutation VARCHAR(125),
	customer_contact_first_name VARCHAR(125),
	customer_contact_last_name VARCHAR(125),
	customer_contact_phone VARCHAR(125),
	currency_code VARCHAR(125),
	website VARCHAR(125),
	opening_balance DECIMAL(20,2),
	opening_balance_exchange_rate DECIMAL(20,2),
	branch_id VARCHAR(125),
	branch_name VARCHAR(125),
	bank_account_payment SMALLINT NOT NULL,
	credit_limit DECIMAL(20,2),
	customer_sub_type VARCHAR(125),
	billing_attention VARCHAR(125),
	billing_address_line_1 VARCHAR(250),
	billing_address_line_2 VARCHAR(250),
	billing_city VARCHAR(125),
	billing_state VARCHAR(125),
	billing_country VARCHAR(125),
	billing_code VARCHAR(125),
	billing_phone VARCHAR(125),
	billing_fax VARCHAR(125),
	shipping_attention VARCHAR(125),
	shipping_address_line_1 VARCHAR(250),
	shipping_address_line_2 VARCHAR(250),
	shipping_city VARCHAR(125),
	shipping_state VARCHAR(125),
	shipping_country VARCHAR(125),
	shipping_code VARCHAR(125),
	shipping_phone VARCHAR(125),
	shipping_fax VARCHAR(125),
	skype_handle VARCHAR(125),
	facebook_handle VARCHAR(125),
	twitter_handle VARCHAR(125),
	department VARCHAR(125),
	designation VARCHAR(125),
	price_list VARCHAR(125),
	payment_terms VARCHAR(125),
	payment_terms_label VARCHAR(125),
	gst_treatment VARCHAR(125),
	gst_identification_number VARCHAR(125),
	owner_name VARCHAR(125),
	primary_contact_id VARCHAR(125),
	email_id VARCHAR(125),
	mobile_phone VARCHAR(125),
	contact_id VARCHAR(125),
	contact_name VARCHAR(125),
	contact_type VARCHAR(125),
	place_of_contact VARCHAR(125),
	place_of_contact_with_state_code VARCHAR(125),
	taxable SMALLINT NOT NULL,
	tax_id VARCHAR(125),
	tax_name VARCHAR(125),
	tax_percentage DECIMAL(20,2),
	exemption_reason VARCHAR(250),
	contact_address_id float4,
	brand VARCHAR(125),
	sales_channel VARCHAR(125),
	cf_msme VARCHAR(125),
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_customer_master_1 FOREIGN KEY (client_id) REFERENCES client_master(id)	
);
	
/*List of all Marketplaces leveraged by Clients*/
DROP TABLE market_place_master;
CREATE TABLE market_place_master (
	id SERIAL PRIMARY KEY,
	marketplace_name VARCHAR(125) NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL
);

/*Has the Clients' subscription details*/
DROP TABLE client_subscriptions;
CREATE TABLE client_subscriptions (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	feature_id INTEGER NOT NULL,
	monthly_license_fees DECIMAL(20,2),
	subscription_end_date TIMESTAMP NOT null,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_client_subscriptions_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_client_subscriptions_2 FOREIGN KEY (feature_id) REFERENCES platform_features_master(id)
);

/*Client specific table - Has the Clients' accounting tool details*/
DROP TABLE evenflow_accounting_details;
CREATE TABLE evenflow_accounting_details (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	invoice_inputs  VARCHAR(125) NOT NULL,
	invoice_number_auto SMALLINT NOT NULL,
	accounting_tool_name VARCHAR(125) NOT NULL,
	accounting_tool_url VARCHAR(125) NOT NULL,
	accounting_tool_userid VARCHAR(125) NOT NULL,
	accounting_tool_pwd VARCHAR(125) NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_accounting_details_1 FOREIGN KEY (client_id) REFERENCES client_master(id)
);

/*Client specific table - Has the Clients' market place details*/
DROP TABLE evenflow_market_place_details;
CREATE TABLE evenflow_market_place_details (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	market_place_master_id INTEGER NOT NULL,
	market_place_url VARCHAR(125) NOT NULL,
	market_place_userid VARCHAR(125) NOT NULL,
	market_place_pwd VARCHAR(125) NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_market_place_details_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_market_place_details_2 FOREIGN KEY (market_place_master_id) REFERENCES market_place_master(id)
);

/*Client specific table - Has details about each Client's product master*/
/*PRAKASH TO RECREATE THIS TABLE*/
DROP TABLE evenflow_product_master cascade;
CREATE TABLE evenflow_product_master (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	item_id float4 NOT NULL,
	item_name varchar(255),
	sku VARCHAR(125),
	hsn_sac INTEGER NOT NULL,
	description VARCHAR(125),
	rate DECIMAL(20,0),
	account VARCHAR(125),
	account_code VARCHAR(125),
	taxable SMALLINT NOT NULL,
	exemption_reason VARCHAR(250),
	taxability_type VARCHAR(125),
	product_type VARCHAR(125),
	parent_category VARCHAR(125),
	intra_state_tax_name VARCHAR(250),
	intra_state_tax_rate DECIMAL(20,2),
	intra_state_tax_type VARCHAR(250),
	inter_state_tax_name VARCHAR(250),
	inter_state_tax_rate DECIMAL(20,2),
	inter_state_tax_type VARCHAR(250),
	source VARCHAR(125),
	reference_id VARCHAR(125),
	status VARCHAR(125),
	usage_unit VARCHAR(125),
	purchase_rate DECIMAL(20,2),
	purchase_account VARCHAR(125),
	purchase_account_code VARCHAR(125),
	purchase_description VARCHAR(125),
	inventory_account VARCHAR(125),
	inventory_account_code VARCHAR(125),
	reorder_point DECIMAL(20,2),
	vendor VARCHAR(125),
	warehouse_name VARCHAR(125),
	opening_stock DECIMAL(20,2),
	opening_stock_value DECIMAL(20,2),
	stock_on_hand DECIMAL(20,2),
	item_type VARCHAR(125),
	is_combo_product SMALLINT NOT NULL DEFAULT 0,
	brand VARCHAR(125),
	sales_channel VARCHAR(125),
	cf_asin VARCHAR(125),
	cf_fsn VARCHAR(125),
	cf_old_sku VARCHAR(125),
	cf_old_asin VARCHAR(125),
	cf_old_fsn VARCHAR(125),
	cf_box_count VARCHAR(125),
	cf_myntra_style_id VARCHAR(125),
	cf_az_tp_excl_gst DECIMAL(20,2),
	cf_mrp_with_tax DECIMAL(20,2),
	cf_fk_tp_excl_gst DECIMAL(20,2),
	cf_instamart_tp_excl_gst DECIMAL(20,2),
	cf_ean VARCHAR(125),
	cf_brands VARCHAR(125),
	cf_blinkit_id VARCHAR(125),
	cf_blinkit_tp numeric(20, 2),
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by VARCHAR(125),
	modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	modified_by	VARCHAR(125),
	active_flag SMALLINT NOT NULL,
	CONSTRAINT fk_evenflow_product_master_1 FOREIGN KEY (client_id) REFERENCES client_master(id)	
);

/*Client specific table - Has details about each Client's Purchase Orders*/
DROP TABLE <clientname>_purchase_orders;
CREATE TABLE evenflow_purchase_orders (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	evenflow_customer_master_id INTEGER NOT NULL,
	sales_orders_id INTEGER,
	po_number VARCHAR(125),
	po_status VARCHAR(125),
	vendor VARCHAR(125),
	ship_to_location VARCHAR(125),
	ordered_on DATE,
	ship_window_from DATE,
	ship_window_to DATE,
	freight_terms VARCHAR(125),
	payment_method VARCHAR(125),
	payment_terms VARCHAR(125),
	purchasing_entity VARCHAR(125),
	submitted_items INTEGER,
	submitted_qty INTEGER,
	submitted_total_cost DECIMAL(20,2),
	accepted_items INTEGER,
	accepted_qty INTEGER,
	accepted_total_cost DECIMAL(20,2),
	cancelled_items INTEGER,
	cancelled_qty INTEGER,
	cancelled_total_cost DECIMAL(20,2),
	received_items INTEGER,
	received_qty INTEGER,
	received_total_cost DECIMAL(20,2),
	delivery_address_to VARCHAR(125),
	delivery_address VARCHAR(250),
	total_qty_requested INTEGER NOT NULL,
	total_qty_accepted INTEGER,
	total_qty_fulfilled INTEGER,
	total_qty_outstanding INTEGER,
	completely_fulfilled  SMALLINT NOT NULL DEFAULT 0,
	fiscal_quarter  VARCHAR(125) NOT NULL, /*eg: Q3, 2024*/
	po_month INTEGER NOT NULL, /*eg: 12*/
	po_year INTEGER NOT NULL, /*eg: 2024*/
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_purchase_orders_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_purchase_orders_2 FOREIGN KEY (evenflow_customer_master_id) REFERENCES evenflow_customer_master(id)	
);

/*Client specific table - Has details about each Client's Purchase Order Line Items*/
DROP TABLE <clientname>_purchase_orders_line_items;
CREATE TABLE evenflow_purchase_orders_line_items (
	id SERIAL PRIMARY KEY,
	evenflow_purchase_orders_id INTEGER NOT NULL,
	asin VARCHAR(125),
	external_id VARCHAR(125),
	model_number VARCHAR(125),
	hsn INTEGER NOT NULL,
	title  VARCHAR(250),
	window_type VARCHAR(125),
	expected_date DATE NOT NULL,
	qty_requested INTEGER NOT NULL,
	qty_accepted INTEGER NOT NULL,
	qty_received INTEGER,
	qty_outstanding INTEGER,
	unit_cost DECIMAL(20,2),
	total_cost DECIMAL(20,2),
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_purchase_orders_line_items_1 FOREIGN KEY (evenflow_purchase_orders_id) REFERENCES evenflow_purchase_orders(id)	
);

/*Client specific table - Has details about each Client's Invoice nputs prepared by Fulfillment team*/
DROP TABLE <clientname>_invoice_inputs;
CREATE TABLE evenflow_invoice_inputs (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	evenflow_customer_master_id INTEGER NOT NULL,
	evenflow_product_master_id INTEGER NOT NULL,
	invoice_number VARCHAR(125),
	estimate_number VARCHAR(125),
	invoice_date VARCHAR(125),
	invoice_status VARCHAR(125) NOT NULL, /*DRAFT*/
	customer_name VARCHAR(125) NOT NULL,
	gst_treatment VARCHAR(125),
	tcs_tax_name VARCHAR(125),
	tcs_percentage DECIMAL(20,2),
	tcs_amount DECIMAL(20,2),
	nature_of_collection VARCHAR(125),
	tcs_payable_account VARCHAR(125),
	tcs_receivable_account VARCHAR(125),
	gstin VARCHAR(125) NOT NULL,
	tds_name VARCHAR(125),
	tds_percentage DECIMAL(20,2),
	tds_section_code VARCHAR(125),
	tds_amount DECIMAL(20,2),
	place_of_supply VARCHAR(125),
	purchase_order_number VARCHAR(125),
	evenflow_purchase_orders_id INTEGER NOT NULL,
	expense_reference_id VARCHAR(125),
	payment_terms VARCHAR(125),
	payment_terms_label VARCHAR(125),
	due_date DATE NOT NULL,
	expected_payment_date DATE NOT NULL,
	sales_person VARCHAR(125),
	shipping_charge_tax_name VARCHAR(125),
	shipping_charge_tax_type VARCHAR(125),
	shipping_charge_tax_percentage DECIMAL(20,2),
	shipping_charge DECIMAL(20,2),
	shipping_charge_tax_exemption_code VARCHAR(125),
	shipping_charge_sac_code VARCHAR(125),
	currency_code VARCHAR(125),
	exchange_rate DECIMAL(20,2),
	account VARCHAR(125),
	item_name VARCHAR(125) NOT NULL,
	sku VARCHAR(125) NOT NULL,
	item_desc VARCHAR(125),
	item_type VARCHAR(125),
	hsn_sac INTEGER NOT NULL,
	quantity DECIMAL(20,2) NOT NULL,
	usage_unit VARCHAR(125) NOT NULL,
	item_price DECIMAL(20,2) NOT NULL,
	item_tax_exemption_reason VARCHAR(250),
	is_inclusive_tax SMALLINT NOT NULL,
	item_tax VARCHAR(125),
	item_tax_type VARCHAR(125),
	item_tax_percentage DECIMAL(20,2),
	reverse_charge_tax_name VARCHAR(125),
	reverse_charge_tax_rate DECIMAL(20,2),
	reverse_charge_tax_type VARCHAR(125),
	project_name VARCHAR(125),
	supply_type VARCHAR(125),
	discount_type VARCHAR(125),
	is_discount_before_tax SMALLINT,
	entity_discount_percent  DECIMAL(20,2),
	entity_discount_amount DECIMAL(20,2),
	discount DECIMAL(20,2),
	discount_amount DECIMAL(20,2),
	adjustment DECIMAL(20,2),
	adjustment_description VARCHAR(250),
	ecommerce_operator_name VARCHAR(125),
	ecommerce_operator_gstin VARCHAR(125),
	paypal SMALLINT,
	razorpay SMALLINT,
	partial_payments SMALLINT,
	template_name VARCHAR(125),
	notes VARCHAR(250),
	terms_conditions VARCHAR(250),
	branch_name VARCHAR(125),
	warehouse_name VARCHAR(125),
	fiscal_quarter  VARCHAR(125) NOT NULL, /*eg: Q3, 2024*/
	po_month INTEGER NOT NULL, /*eg: 12*/
	po_year INTEGER NOT NULL, /*eg: 2024*/
	payment_received SMALLINT,
	appointment_id VARCHAR(125),
	appointment_date DATE,
	accepted_qty INTEGER,
	evenflow_warehouses_id INTEGER,
	invoice_generated_acc_tool SMALLINT NOT NULL DEFAULT 0, /*0-Not yet generated in the acc tool; 1-Generated; 2-Failed to generate*/
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_invoice_inputs_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_invoice_inputs_2 FOREIGN KEY (evenflow_customer_master_id) REFERENCES evenflow_customer_master(id),
	CONSTRAINT fk_evenflow_invoice_inputs_3 FOREIGN KEY (evenflow_purchase_orders_id) REFERENCES evenflow_purchase_orders(id),
	CONSTRAINT fk_evenflow_invoice_inputs_4 FOREIGN KEY (evenflow_product_master_id) REFERENCES evenflow_product_master(id),
	CONSTRAINT fk_evenflow_invoice_inputs_5 FOREIGN KEY (evenflow_warehouses_id) REFERENCES evenflow_warehouses(id)
);


select * from evenflow_invoices
/*Client specific table - Has details about each Client's Invoice inputs prepared by FinOps team*/
DROP TABLE <clientname>_invoices;
CREATE TABLE evenflow_invoices (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	evenflow_customer_master_id INTEGER NOT NULL,
	evenflow_product_master_id INTEGER NOT NULL,
	evenflow_invoice_inputs_id INTEGER NOT NULL,
	invoice_number VARCHAR(125) NOT NULL,
	estimate_number VARCHAR(125),
	invoice_date VARCHAR(125) NOT NULL,
	invoice_status VARCHAR(125) NOT NULL,
	customer_name VARCHAR(125) NOT NULL,
	gst_treatment VARCHAR(125),
	tcs_tax_name VARCHAR(125),
	tcs_percentage DECIMAL(20,2),
	tcs_amount DECIMAL(20,2),
	nature_of_collection VARCHAR(125),
	tcs_payable_account VARCHAR(125),
	tcs_receivable_account VARCHAR(125),
	gstin VARCHAR(125) NOT NULL,
	tds_name VARCHAR(125),
	tds_percentage DECIMAL(20,2),
	tds_section_code VARCHAR(125),
	tds_amount DECIMAL(20,2),
	place_of_supply VARCHAR(125),
	purchase_order_number VARCHAR(125),
	evenflow_purchase_orders_id INTEGER NOT NULL,
	expense_reference_id VARCHAR(125),
	payment_terms VARCHAR(125),
	payment_terms_label VARCHAR(125),
	due_date DATE NOT NULL,
	expected_payment_date DATE NOT NULL,
	sales_person VARCHAR(125),
	shipping_charge_tax_name VARCHAR(125),
	shipping_charge_tax_type VARCHAR(125),
	shipping_charge_tax_percentage DECIMAL(20,2),
	shipping_charge DECIMAL(20,2),
	shipping_charge_tax_exemption_code VARCHAR(125),
	shipping_charge_sac_code VARCHAR(125),
	currency_code VARCHAR(125),
	exchange_rate DECIMAL(20,2),
	account VARCHAR(125),
	item_name VARCHAR(125) NOT NULL,
	sku VARCHAR(125) NOT NULL,
	item_desc VARCHAR(125),
	item_type VARCHAR(125),
	hsn_sac INTEGER NOT NULL,
	quantity DECIMAL(20,2) NOT NULL,
	usage_unit VARCHAR(125) NOT NULL,
	item_price DECIMAL(20,2) NOT NULL,
	item_tax_exemption_reason VARCHAR(250),
	is_inclusive_tax SMALLINT NOT NULL,
	item_tax VARCHAR(125),
	item_tax_type VARCHAR(125),
	item_tax_percentage DECIMAL(20,2),
	reverse_charge_tax_name VARCHAR(125),
	reverse_charge_tax_rate DECIMAL(20,2),
	reverse_charge_tax_type VARCHAR(125),
	project_name VARCHAR(125),
	supply_type VARCHAR(125),
	discount_type VARCHAR(125),
	is_discount_before_tax SMALLINT,
	entity_discount_percent  DECIMAL(20,2),
	entity_discount_amount DECIMAL(20,2),
	discount DECIMAL(20,2),
	discount_amount DECIMAL(20,2),
	adjustment DECIMAL(20,2),
	adjustment_description VARCHAR(250),
	ecommerce_operator_name VARCHAR(125),
	ecommerce_operator_gstin VARCHAR(125),
	paypal SMALLINT,
	razorpay SMALLINT,
	partial_payments SMALLINT,
	template_name VARCHAR(125),
	notes VARCHAR(250),
	terms_conditions VARCHAR(250),
	branch_name VARCHAR(125),
	evenflow_warehouses_id INTEGER,	
	warehouse_name VARCHAR(125),
	fiscal_quarter  VARCHAR(125) NOT NULL, /*eg: Q3, 2024*/
	po_month INTEGER NOT NULL, /*eg: 12*/
	po_year INTEGER NOT NULL, /*eg: 2024*/
	payment_received SMALLINT NOT NULL DEFAULT 0,
	ageing_days INTEGER,
	invoice_generated_acc_tool SMALLINT NOT NULL DEFAULT 0, /*0-Not yet generated in the acc tool; 1-Generated; 2-Failed to generate*/
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_invoices_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_invoices_2 FOREIGN KEY (evenflow_customer_master_id) REFERENCES evenflow_customer_master(id),
	CONSTRAINT fk_evenflow_invoices_3 FOREIGN KEY (evenflow_purchase_orders_id) REFERENCES evenflow_purchase_orders(id),
	CONSTRAINT fk_evenflow_invoices_4 FOREIGN KEY (evenflow_product_master_id) REFERENCES evenflow_product_master(id),
	CONSTRAINT fk_evenflow_invoices_5 FOREIGN KEY (evenflow_invoice_inputs_id) REFERENCES evenflow_invoice_inputs(id),
	CONSTRAINT fk_evenflow_invoices_6 FOREIGN KEY (evenflow_warehouses_id) REFERENCES evenflow_warehouses(id)
);

/*Client specific table - Has details about each Client's Invoice payments*/
DROP TABLE <clientname>_invoice_payments;
CREATE TABLE evenflow_invoice_payments (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	evenflow_customer_master_id INTEGER NOT NULL,
	evenflow_invoice_id INTEGER NOT NULL,
	evenflow_invoice_number VARCHAR(125),
	invoice_number VARCHAR(125) NOT NULL,
	payment_number VARCHAR(125) NOT NULL,
	invoice_date DATE NOT NULL,
	transaction_type VARCHAR(125) NOT NULL,
	transaction_description VARCHAR(250),
	reference_details VARCHAR(125) NOT NULL,
	original_invoice_number VARCHAR(125),
	invoice_amount DECIMAL(20,2) NOT NULL,
	invoice_currency VARCHAR(125) NOT NULL,
	withholding_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	terms_discount_taken DECIMAL(20,2) NOT NULL DEFAULT 0,
	amount_paid DECIMAL(20,2) NOT NULL DEFAULT 0,
	remaining_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_invoice_payments_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_invoice_payments_2 FOREIGN KEY (evenflow_customer_master_id) REFERENCES evenflow_customer_master(id),
	CONSTRAINT fk_evenflow_invoice_payments_3 FOREIGN KEY (evenflow_invoice_id) REFERENCES evenflow_invoices(id)--,
	--CONSTRAINT fk_evenflow_invoice_payments_4 FOREIGN KEY (evenflow_invoice_number) REFERENCES evenflow_invoices(invoice_number)
);

/*Client specific table - Aggregations of POs as per their Status, Buyer & Fiscal Quarter*/
DROP TABLE <clientname>_agg_po_invoices;
CREATE TABLE evenflow_agg_po_invoices (
	id SERIAL PRIMARY KEY,
	client_id INTEGER NOT NULL,
	calendar_month INTEGER NOT NULL, /*eg: 12*/
	calendar_year INTEGER NOT NULL, /*eg: 2024*/
	fiscal_quarter VARCHAR(125) NOT NULL, /*eg: Q3, 2024*/
	evenflow_customer_master_id INTEGER NOT NULL,
	customer_name VARCHAR(125), /*buyer name*/
	received_po INTEGER NOT NULL DEFAULT 0,
	received_po_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	partially_fulfilled_po INTEGER NOT NULL DEFAULT 0,
	partially_fulfilled_po_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	completely_fulfilled_po INTEGER NOT NULL DEFAULT 0,
	completely_fulfilled_po_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	open_po INTEGER NOT NULL DEFAULT 0, /*PO has been approved but Invoice Inputs have not been created yet*/
	open_po_amount DECIMAL(20,2) NOT NULL DEFAULT 0, /*PO has been approved but Invoice Inputs have not been created yet*/
	raised_invoices INTEGER NOT NULL DEFAULT 0,
	raised_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	settled_invoices INTEGER NOT NULL DEFAULT 0,
	settled_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	total_pending_invoices INTEGER NOT NULL DEFAULT 0,
	total_pending_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	overdue_invoices INTEGER NOT NULL DEFAULT 0,
	overdue_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	due_invoices INTEGER NOT NULL DEFAULT 0,
	due_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,
	due_next7days_invoices INTEGER NOT NULL DEFAULT 0,
	due_next7days_invoices_amount DECIMAL(20,2) NOT NULL DEFAULT 0,		
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_evenflow_agg_po_invoices_1 FOREIGN KEY (client_id) REFERENCES client_master(id),
	CONSTRAINT fk_evenflow_agg_po_invoices_2 FOREIGN KEY (evenflow_customer_master_id) REFERENCES evenflow_customer_master(id)
);

/*Roles table*/
DROP TABLE roles;
CREATE TABLE roles (
	id SERIAL PRIMARY KEY,
	role_name VARCHAR(125) NOT NULL,
	role_description VARCHAR(250) NOT NULL,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1
);

/*Users table*/
DROP TABLE users;
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	user_first_name VARCHAR(125) NOT NULL,
	user_last_name VARCHAR(125) NOT NULL,
	user_e_mail_id VARCHAR(125),
	user_phone_number VARCHAR(125),
	user_login_id VARCHAR(125) NOT NULL,
	user_password VARCHAR(250) NOT NULL,
	client_id INTEGER NOT NULL,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_users_1 FOREIGN KEY (client_id) REFERENCES client_master(id)
);

/*User Role Mapping table*/
DROP TABLE user_roles;
CREATE TABLE user_roles (
	id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL,
	role_id INTEGER NOT NULL,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_user_roles_1 FOREIGN KEY (user_id) REFERENCES users(id),
	CONSTRAINT fk_user_roles_2 FOREIGN KEY (role_id) REFERENCES roles(id)
);

/*Screens (Menu Items) table*/
DROP TABLE screens;
CREATE TABLE screens (
	id SERIAL PRIMARY KEY,
	screen_id INTEGER NOT NULL,
	screen_name VARCHAR(125) NOT NULL,
	screen_description VARCHAR(250) NOT NULL,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1
);

/*Features (Screens/Menu Items) Access Privileges table*/
DROP TABLE feature_privileges;
CREATE TABLE feature_privileges (
	id SERIAL PRIMARY KEY,
	screen_id INTEGER NOT NULL,
	privilege_type VARCHAR(125) NOT NULL, /*READ, SAVE, CAPTURE_PAYMENTS, etc*/
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT feature_privileges_1 FOREIGN KEY (screen_id) REFERENCES screens(id)
);

/*Feature Access Privilege to Roles Mapping table*/
DROP TABLE roles_feature_privileges;
CREATE TABLE roles_feature_privileges (
	id SERIAL PRIMARY KEY,
	screen_id INTEGER NOT NULL,
	role_id INTEGER NOT NULL,
	feature_privileges_id INTEGER NOT NULL,
	privilege_access SMALLINT NOT NULL DEFAULT 0,
	created_on TIMESTAMP DEFAULT NULL,
	created_by VARCHAR(125) DEFAULT NULL,
	modified_on TIMESTAMP DEFAULT NULL,
	modified_by VARCHAR(125) DEFAULT NULL,
	active_flag SMALLINT NOT NULL DEFAULT 1,
	CONSTRAINT fk_roles_feature_privileges_1 FOREIGN KEY (screen_id) REFERENCES screens(id),
	CONSTRAINT fk_roles_feature_privileges_2 FOREIGN KEY (role_id) REFERENCES roles(id),
	CONSTRAINT fk_roles_feature_privileges_3 FOREIGN KEY (feature_privileges_id) REFERENCES feature_privileges(id)
);
	
CREATE TABLE user_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_tokens_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
