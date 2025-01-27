from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    SmallInteger,
    ForeignKey,
    Float,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_first_name = Column(String(125), nullable=False)
    user_last_name = Column(String(125), nullable=False)
    user_e_mail_id = Column(String(125), nullable=True)
    user_phone_number = Column(String(125), nullable=True)
    user_login_id = Column(String(125), nullable=False, unique=True)
    user_password = Column(String(250), nullable=False)
    client_id = Column(Integer, ForeignKey("client_master.id", ondelete="CASCADE"), nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now)
    created_by = Column(String(125), nullable=True)
    modified_on = Column(TIMESTAMP, nullable=True, onupdate=datetime.now)
    modified_by = Column(String(125), nullable=True)
    active_flag = Column(SmallInteger, nullable=False, default=1)

    # Relationship with UserRole
    user_roles = relationship("UserRole", back_populates="user")

    # Relationship with user tokens
    tokens = relationship("UserTokens", back_populates="user", cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(125), nullable=False)
    role_description = Column(String(250), nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now)
    created_by = Column(String(125), nullable=True)
    modified_on = Column(TIMESTAMP, nullable=True, onupdate=datetime.now)
    modified_by = Column(String(125), nullable=True)
    active_flag = Column(SmallInteger, nullable=False, default=1)

    # Relationship with UserRole
    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now)
    created_by = Column(String(125), nullable=True)
    modified_on = Column(TIMESTAMP, nullable=True, onupdate=datetime.now)
    modified_by = Column(String(125), nullable=True)
    active_flag = Column(SmallInteger, nullable=False, default=1)

    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

class ClientMaster(Base):
    __tablename__ = "client_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(125), nullable=False)
    pan = Column(String(125), nullable=False)
    gst = Column(String(125), nullable=False)
    client_reg_address_line_1 = Column(String(250), nullable=False)
    client_reg_address_line_2 = Column(String(250), nullable=True)
    client_reg_city = Column(String(125), nullable=False)
    client_reg_state = Column(String(125), nullable=False)
    client_reg_country = Column(String(125), nullable=False)
    url = Column(String(125), nullable=True)
    created_on = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created_by = Column(String(125), nullable=True)
    modified_on = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)
    modified_by = Column(String(125), nullable=True)
    active_flag = Column(SmallInteger, default=1, nullable=False)

class DistyMaster(Base):
    __tablename__ = "disty_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(125), nullable=False)
    pan = Column(String(125), nullable=True)
    gst = Column(String(125), nullable=True)
    registered_address_line_1 = Column(String(250), nullable=True)
    registered_address_line_2 = Column(String(250), nullable=True)
    registered_city = Column(String(125), nullable=True)
    registered_state = Column(String(125), nullable=True)
    registered_country = Column(String(125), nullable=True)
    created_on = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created_by = Column(String(125), nullable=True)
    modified_on = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)
    modified_by = Column(String(125), nullable=True)
    active_flag = Column(SmallInteger, default=1, nullable=False)

class EvenflowDistys(Base):
    __tablename__ = "evenflow_distys"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client_master.id"), nullable=False)
    disty_id = Column(Integer, ForeignKey("disty_master.id"), nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now)
    created_by = Column(String(125), default="bhagavan")
    modified_on = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(String(125), default="bhagavan")
    active_flag = Column(SmallInteger, default=1, nullable=False)


class AccountingDetails(Base):
    __tablename__ = "evenflow_accounting_details"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client_master.id"), nullable=False)
    invoice_inputs = Column(String(125), nullable=False)
    invoice_number_auto = Column(SmallInteger, nullable=False)
    accounting_tool_name = Column(String(125), nullable=False)
    accounting_tool_url = Column(String(125), nullable=False)
    accounting_tool_userid = Column(String(125), nullable=False)
    accounting_tool_pwd = Column(String(125), nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now)
    created_by = Column(String(125), default="bhagavan")
    modified_on = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(String(125), default="bhagavan")
    active_flag = Column(SmallInteger, default=1, nullable=False)

class UserTokens(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    created_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    modified_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    modified_by = Column(String, nullable=True)
    active_flag = Column(SmallInteger, nullable=False, default=1)  # Add active_flag with a default value

    # Relationship with User
    user = relationship("User", back_populates="tokens")

class EvenflowCustomerMaster(Base):
    __tablename__ = 'evenflow_customer_master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client_master.id'), nullable=False)
    customer_name = Column(String(125), nullable=False)
    customer_contact_salutation = Column(String(125))
    customer_contact_first_name = Column(String(125))
    customer_contact_last_name = Column(String(125))
    customer_contact_phone = Column(String(125))
    currency_code = Column(String(125))
    website = Column(String(125))
    opening_balance = Column(DECIMAL(20, 2), default=0.0)
    opening_balance_exchange_rate = Column(DECIMAL(20, 2), default=1.0)
    branch_id = Column(String(125))
    branch_name = Column(String(125))
    bank_account_payment = Column(SmallInteger, nullable=False, default=1)
    credit_limit = Column(DECIMAL(20, 2), default=0.0)
    customer_sub_type = Column(String(125))
    billing_attention = Column(String(125))
    billing_address_line_1 = Column(String(250))
    billing_address_line_2 = Column(String(250))
    billing_city = Column(String(125))
    billing_state = Column(String(125))
    billing_country = Column(String(125))
    billing_code = Column(String(125))
    billing_phone = Column(String(125))
    billing_fax = Column(String(125))
    shipping_attention = Column(String(125))
    shipping_address_line_1 = Column(String(250))
    shipping_address_line_2 = Column(String(250))
    shipping_city = Column(String(125))
    shipping_state = Column(String(125))
    shipping_country = Column(String(125))
    shipping_code = Column(String(125))
    shipping_phone = Column(String(125))
    shipping_fax = Column(String(125))
    skype_handle = Column(String(125))
    facebook_handle = Column(String(125))
    twitter_handle = Column(String(125))
    department = Column(String(125))
    designation = Column(String(125))
    price_list = Column(String(125))
    payment_terms = Column(String(125))
    payment_terms_label = Column(String(125))
    gst_treatment = Column(String(125))
    gst_identification_number = Column(String(125))
    owner_name = Column(String(125))
    primary_contact_id = Column(String(125))
    email_id = Column(String(125))
    mobile_phone = Column(String(125))
    contact_id = Column(String(125))
    contact_name = Column(String(125))
    contact_type = Column(String(125))
    place_of_contact = Column(String(125))
    place_of_contact_with_state_code = Column(String(125))
    taxable = Column(SmallInteger, nullable=False, default=1)
    tax_id = Column(String(125))
    tax_name = Column(String(125))
    tax_percentage = Column(DECIMAL(20, 2), default=0.0)
    exemption_reason = Column(String(250))
    contact_address_id = Column(Float)
    brand = Column(String(125))
    sales_channel = Column(String(125))
    cf_msme = Column(String(125))
    created_on = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(125))
    modified_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String(125))
    active_flag = Column(SmallInteger, nullable=False, default=1)


class EvenflowProductMaster(Base):
    __tablename__ = 'evenflow_product_master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client_master.id'), nullable=False)
    item_id = Column(Float, nullable=False)
    item_name = Column(String(255))
    sku = Column(String(125))
    hsn_sac = Column(Integer, nullable=False)
    description = Column(String(125))
    rate = Column(DECIMAL(20, 0))
    account = Column(String(125))
    account_code = Column(String(125))
    taxable = Column(SmallInteger, nullable=False)
    exemption_reason = Column(String(250))
    taxability_type = Column(String(125))
    product_type = Column(String(125))
    parent_category = Column(String(125))
    intra_state_tax_name = Column(String(250))
    intra_state_tax_rate = Column(DECIMAL(20, 2))
    intra_state_tax_type = Column(String(250))
    inter_state_tax_name = Column(String(250))
    inter_state_tax_rate = Column(DECIMAL(20, 2))
    inter_state_tax_type = Column(String(250))
    source = Column(String(125))
    reference_id = Column(String(125))
    status = Column(String(125))
    usage_unit = Column(String(125))
    purchase_rate = Column(DECIMAL(20, 2))
    purchase_account = Column(String(125))
    purchase_account_code = Column(String(125))
    purchase_description = Column(String(125))
    inventory_account = Column(String(125))
    inventory_account_code = Column(String(125))
    reorder_point = Column(DECIMAL(20, 2))
    vendor = Column(String(125))
    warehouse_name = Column(String(125))
    opening_stock = Column(DECIMAL(20, 2))
    opening_stock_value = Column(DECIMAL(20, 2))
    stock_on_hand = Column(DECIMAL(20, 2))
    item_type = Column(String(125))
    is_combo_product = Column(SmallInteger, nullable=False, default=0)
    brand = Column(String(125))
    sales_channel = Column(String(125))
    cf_asin = Column(String(125))
    cf_fsn = Column(String(125))
    cf_old_sku = Column(String(125))
    cf_old_asin = Column(String(125))
    cf_old_fsn = Column(String(125))
    cf_box_count = Column(String(125))
    cf_myntra_style_id = Column(String(125))
    cf_az_tp_excl_gst = Column(DECIMAL(20, 2))
    cf_mrp_with_tax = Column(DECIMAL(20, 2))
    cf_fk_tp_excl_gst = Column(DECIMAL(20, 2))
    cf_instamart_tp_excl_gst = Column(DECIMAL(20, 2))
    cf_ean = Column(String(125))
    cf_brands = Column(String(125))
    cf_blinkit_id = Column(String(125))
    cf_blinkit_tp = Column(DECIMAL(20, 2))
    created_on = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(125))
    modified_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String(125))
    active_flag = Column(SmallInteger, nullable=False)
