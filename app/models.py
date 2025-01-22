from sqlalchemy import Column, Integer, String, TIMESTAMP, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
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
