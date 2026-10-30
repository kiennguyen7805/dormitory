from datetime import date
import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailValidatedModel(BaseModel):
    @field_validator("email", check_fields=False)
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError("Email không đúng định dạng.")
        return normalized


class LoginRequest(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool = True


class UserCreate(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    role: str


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    role: str
    is_active: bool


class StudentProfileUpdate(BaseModel):
    student_code: str = Field(min_length=1, max_length=30)
    faculty: str = Field(default="", max_length=150)
    cohort: str = Field(default="", max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, pattern="^(Male|Female|Other)$")
    phone: str = Field(default="", max_length=30)
    address: str = Field(default="", max_length=300)
    identity_number: str | None = Field(default=None, max_length=30)
    emergency_contact_name: str = Field(default="", max_length=120)
    emergency_contact_phone: str = Field(default="", max_length=30)


class StudentProfileRead(StudentProfileUpdate):
    user_id: UUID
    email: str
    full_name: str


class RegisterRequest(EmailValidatedModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    student_code: str = Field(min_length=8, max_length=8, pattern=r"^\S{8}$")
    age: int = Field(ge=18, le=60)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=32, max_length=512)


class StudentCreate(RegisterRequest):
    pass


class StudentRead(BaseModel):
    id: UUID
    student_code: str
    full_name: str
    age: int | None
    email: str
    is_active: bool


class StudentPage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[StudentRead]
    page: int
    page_size: int = Field(serialization_alias="pageSize")
    total: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead
