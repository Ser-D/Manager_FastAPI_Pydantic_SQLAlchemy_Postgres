from datetime import date
from pydantic import Field, EmailStr, BaseModel, PastDatetime

class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=50)
    email: str = EmailStr()
    phone: str = Field(min_length=3, max_length=25)
    birthday: str = PastDatetime()
    info: str | None = Field(max_length=250, nullable=True)


class ContactResponseSchema(BaseModel):
    id: int 
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    info: str