from datetime import date, datetime
from pydantic import Field, EmailStr, BaseModel, field_validator


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=50)
    email: str = EmailStr
    phone: str = Field(min_length=3, max_length=25)
    birthday: date = Field()
    info: str = Field(max_length=250, nullable=True)

    @field_validator('birthday')
    def future_date_filter(cls, value_date):
        if value_date > datetime.now().date():
            raise ValueError("birthday date can't be in future")
        return value_date


class ContactResponseSchema(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    info: str


class ContactUpdateSchema(ContactSchema):
    pass
