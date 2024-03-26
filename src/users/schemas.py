from pydantic import Field, EmailStr, BaseModel, PastDatetime

class UserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=50)
    email: str = EmailStr()
    birthday: str = PastDatetime()
    info: str | None = Field(max_length=250, nullable=True)


class UserResponseSchema(BaseModel):
    id: int 
    name: str
    surname: str
    email: EmailStr
    birthday: PastDatetime
    info: str