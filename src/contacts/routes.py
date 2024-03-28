from fastapi import APIRouter, Depends, Query, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_postgresql import get_database

from src.contacts.schemas import ContactResponseSchema, ContactSchema
from src.contacts.models import ContactModel
from src.contacts import todos

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponseSchema])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db=Depends(get_database)):
    contacts = await todos.get_contacts(limit, offset, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponseSchema)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_database)):
    contact = await todos.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
    return contact


@router.post('/', response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_database)):
    contact = await todos.create_contact(body, db)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_database)):
    contact = await todos.delete_contact(contact_id, db)
    return contact
