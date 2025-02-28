from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class UserBase(BaseModel):
    username: str
    role: str
    client: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    user_first_name: str
    user_last_name: str
    user_e_mail_id: Optional[str] = None
    user_phone_number: Optional[str] = None
    user_login_id: str
    client_id: int

    class Config:
        orm_mode = True


class DistyInput(BaseModel):
    disty_id: int


class AccountingToolDetails(BaseModel):
    id: int
    accounting_tool_name: str

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models directly


class ClientOnboardingRequest(BaseModel):
    b2b_distributors: List[DistyInput]
    accounting_tool_details: AccountingToolDetails


class UserTokenSchema(BaseModel):
    id: int
    user_id: int
    token: str
    created_on: datetime
    active_flag: int


class UploadPoSchema(BaseModel):
    filename: str
    # file_hash: str
    saved_path: str
    status: str
    extracted_data: Optional[List[dict]] = None


class DistyMasterSchema(BaseModel):
    id: int
    name: str


class ClientMasterSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AccountingDetailsSchema(BaseModel):
    id: int
    name: str


class AccountingDetails(BaseModel):
    url: HttpUrl
    username: str
    password: str


class ClientDetails(BaseModel):
    id: int
    distributors: List[int]
    accountingtool: str
    priority: Optional[str] = None
    generateinvoice: bool
    accountingDetails: AccountingDetails


class MappingItem(BaseModel):
    sourceField: str
    targetField: str
    value: Optional[str] = None


class ClientOnboardRequest(BaseModel):
    client_details: ClientDetails
    po_mapping: List[MappingItem]
    itemmaster_mapping: List[MappingItem]
    customermaster_mapping: List[MappingItem]

class user_nameAndOTPSchema(BaseModel):
    user_name: str
    otp: int  # otp field to match the model
    generated_at: datetime  # Add generated_at to match the model
    valid_until: datetime  # Add valid_until to match the model
   
   
   
    class Config:
        orm_mode = True


class user_nameAndOTPSchema(BaseModel):
    user_name: str
    otp: int  # otp field to match the model
    generated_at: datetime  # Add generated_at to match the model
    valid_until: datetime  # Add valid_until to match the model
   
   
   
    class Config:
        orm_mode = True




#------------------------------Invoice generation Flow Schemas------------------------------------
class GenerateInvoiceRequest(BaseModel):
    invoiceNumber: str


class InvoiceInputRecord(BaseModel):
    invoiceInputsId: int
    invoiceNumber: Optional[str]
    customerName: str
    invoiceAmount: Optional[float]
    paymentDueDate: Optional[str]
    paymentTerms: str
    poFilePath: str
    invoiceInputs: str

class InvoiceInputResponse(BaseModel):
    invoiceInputsRecordCount: dict[str, int]
    invoiceInputsRecords: list[InvoiceInputRecord]


class PORecord(BaseModel):
    purchaseOrderId: int
    poNumber: str

class POResponse(BaseModel):
    poRecordCount: dict[str, int]
    poRecords: list[PORecord]


class InvoiceInputUpdate(BaseModel):
    id: int = Field(..., alias="invoiceInputsId")
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")
    invoice_date: Optional[str] = Field(None, alias="invoiceDate")
    invoice_amount: Optional[float] = Field(None, alias="invoiceAmount")
    expected_due_date: Optional[str] = Field(None, alias="paymentDueDate")


class InvoiceInputsUpdateRequest(BaseModel):
    updates: list[InvoiceInputUpdate]

class InvoiceInputsUpdateResponse(BaseModel):
    message: str
    updatedRecords: list[dict]

class GenerateInvoiceRequest(BaseModel):
    invoiceNumber: str



class PORecord(BaseModel):
    purchaseOrderId: int
    poNumber: str





from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import date

class CustomField(BaseModel):
    customfield_id: str
    value: Union[str, int]

class InvoiceLineItem(BaseModel):
    item_id: int
    hsn_or_sac: int
    item_order: int
    quantity: int
    unit: str
    rate: float

class Invoice(BaseModel):
    customer_id: int
    invoice_number: str
    place_of_supply: str
    gst_treatment: str
    gst_no: str
    date: date
    payment_terms: int
    payment_terms_label: str
    is_inclusive_tax: bool
    custom_fields: List[CustomField]
    line_items: List[InvoiceLineItem]
    notes: Optional[str]


class EwayBillUpdateRequest(BaseModel):
    id: int
    invoiceNumber: str
    ewayBillNumber: Optional[str] = None
    transportProviderName: Optional[str] = None
    transportProviderContact: Optional[str] = None
    transportProviderVehicleNumber: Optional[str] = None
    notes: Optional[str] = None


class GenerateEwayBillRequest(BaseModel):
    ewayBillNumber: str