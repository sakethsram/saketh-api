from pydantic import BaseModel
from pydantic import HttpUrl
from typing import Optional
from typing import List
from datetime import datetime



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

from pydantic import BaseModel

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
     
