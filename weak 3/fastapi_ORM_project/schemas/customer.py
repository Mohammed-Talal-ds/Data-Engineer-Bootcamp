from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    class Config:
        orm_mode = True