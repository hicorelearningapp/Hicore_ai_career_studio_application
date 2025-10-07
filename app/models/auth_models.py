from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import RoleEnum

class AuthRequest(BaseModel):
    provider: str
    role: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    otp: Optional[str] = None
    token: Optional[str] = None   # Google ID Token
    code: Optional[str] = None    # LinkedIn auth code

class OTPRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    def validate_contact(self):
        if not (self.phone or self.email):
            raise ValueError("Either phone or email must be provided")

class OTPVerify(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    otp: str

    def validate_contact(self):
        if not (self.phone or self.email):
            raise ValueError("Either phone or email must be provided")
