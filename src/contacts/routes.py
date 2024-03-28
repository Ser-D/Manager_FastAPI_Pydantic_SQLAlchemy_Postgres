from fastapi import APIRouter, Depends, Query, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_postgresql import get_database

from src.contacts.schemas import ContactResponseSchema, ContactSchema, ContactUpdateSchema
from src.contacts.models import ContactModel
from src.contacts import repository

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponseSchema])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db=Depends(get_database)):
    contacts = await repository.get_contacts(limit, offset, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponseSchema)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_database)):
    contact = await repository.get_contact(contact_id, db)
    print(contact)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
    return contact


@router.post('/', response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_database)):
    contact = await repository.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1),
                         db: AsyncSession = Depends(get_database),
                         ):
    contact = await repository.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_database)):
    contact = await repository.delete_contact(contact_id, db)
    return contact


@router.get("/find/{query}", response_model=list[ContactResponseSchema])
async def find_contact(query: str, db: AsyncSession = Depends(get_database)):
    contacts = await repository.find_contacts(query, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts


@router.get("/upcoming_birthdays/", response_model=list[ContactResponseSchema])
async def upcoming_birthday(db: AsyncSession = Depends(get_database)):
    contacts = await repository.upcoming_birthday(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts
