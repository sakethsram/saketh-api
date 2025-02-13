from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


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
    file_hash: str
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

class InvoiceInputRecord(BaseModel):
    invoiceInputsId: int
    invoiceNumber: Optional[str]
    customerName: str
    invoiceAmount: Optional[float]
    paymentDueDate: Optional[str]
    paymentTerms: str
    poFilePath: str
    invoiceInputs: str

class PORecord(BaseModel):
    purchaseOrderId: int
    poNumber: str
