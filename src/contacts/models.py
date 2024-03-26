from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ContactModel(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(75), unique=True)
    phone: Mapped[str] = mapped_column(String(25), unique=True)
    birthday: Mapped[Date] = mapped_column(Date)
    info: Mapped[str] = mapped_column(String(250), nullable=True)