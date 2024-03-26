from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from contacts.models import ContactModel
from contacts.schemas import ContactResponseSchema, ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(ContactModel).offset(offset).limit(limit)
    todos = db.execute(stmt)
    return todos.scalars().all()