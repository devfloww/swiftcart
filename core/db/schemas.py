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