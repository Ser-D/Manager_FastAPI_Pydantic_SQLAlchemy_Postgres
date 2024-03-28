from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import ContactModel
from src.contacts.schemas import ContactResponseSchema, ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(ContactModel).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(ContactModel).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = ContactModel(**body.model_dump(exclude_unset=True))  # (name=body.name, phone=body.phone, ...)
    db.add(contact)
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