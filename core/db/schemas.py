from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import enum

# User Model Schemas
class UserRole(enum.StrEnum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    ADMIN = "admin"

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.CUSTOMER
    
    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password Must contain at least ONE uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password Must contain at least ONE lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password Must contain at least ONE digit")
        return v
 
class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class VendorCreate(BaseModel):
    user_id: int
    store_name: str = Field(..., min_length=2, max_length=100)
    store_slug: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=255)
    contact_number: str = Field(..., min_length=7, max_length=20)
    description: Optional[str] = Field(None, max_length=1000)
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
        
class VendorRead(BaseModel):
    id: int
    user_id: int
    store_name: str
    store_slug: str
    address: str
    contact_number: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    is_approved: Optional[bool] = None
    approved_at: datetime
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True