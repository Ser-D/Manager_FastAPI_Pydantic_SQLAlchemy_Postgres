from datetime import date, timedelta

from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import ContactModel
from src.contacts.schemas import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(ContactModel).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(ContactModel).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = ContactModel(
        **body.model_dump(exclude_unset=True, exclude_defaults=True))  # (name=body.name, phone=body.phone, ...)
    db.add(contact)
    try:
        await db.commit()
        await db.refresh(contact)
        return contact
    except Exception as err:
        return None



async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    stmt = select(ContactModel).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.info = body.info
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(ContactModel).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def find_contacts(query: str, db: AsyncSession):
    stmt = select(ContactModel).filter(or_(
        ContactModel.name.ilike(f"%{query}%"),
        ContactModel.surname.ilike(f"%{query}"),
        ContactModel.email.ilike(f"%{query}%"),
        ContactModel.phone.ilike(f"%{query}%")
    )
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def upcoming_birthday(db: AsyncSession):
    current_date = date.today()
    next_week = current_date + timedelta(days=7)
    stmt = select(ContactModel).filter(and_(
        extract("month", ContactModel.birthday) >= current_date.month,
        extract("day", ContactModel.birthday) >= current_date.day,
        extract("month", ContactModel.birthday) <= next_week.month,
        extract("day", ContactModel.birthday) <= next_week.day
    )
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()
