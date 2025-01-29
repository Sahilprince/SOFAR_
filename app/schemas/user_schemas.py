# app/schemas/user_schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=3, max_length=50)
    role: UserRole = UserRole.STUDENT
    phone_number: Optional[str] = Field(None, min_length=10, max_length=10, pattern="^[0-9]+$")

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponseDTO(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    
class AdminCreateDTO(UserCreateDTO):
    """
    AdminCreateDTO inherits all fields from UserCreateDTO.
    Additional admin-specific validation can be added here if needed.
    """
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone_number: str = Field(..., min_length=10, max_length=10, pattern="^[0-9]+$") 