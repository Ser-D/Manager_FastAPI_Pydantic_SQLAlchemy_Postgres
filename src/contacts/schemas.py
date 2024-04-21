import re
from datetime import date, datetime
from pydantic import Field, EmailStr, BaseModel, field_validator, ConfigDict

from src.users.schemas import UserResponseSchema


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=50)
    email: str = Field()
    phone: str = Field(min_length=3, max_length=25)
    birthday: date = Field()
    info: str = Field(max_length=250, nullable=True)

    @field_validator('email')
    def email_cheacker(cls, value_email):
        if re.search(r'[\w.-]+@[\w.-]+', value_email):
            return value_email
        raise ValueError("Invalid email")

    @field_validator('birthday')
    def future_date_filter(cls, value_date):
        if value_date > datetime.now().date():
            raise ValueError("birthday date can't be in future")
        return value_date


class ContactResponseSchema(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: str
    phone: str
    birthday: date
    info: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponseSchema | None

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True


class ContactUpdateSchema(ContactSchema):
    pass
