from fastapi import APIRouter, Depends, Query

from database.db_sqlite import get_database

from contacts.schemas import ContactResponseSchema, ContactSchema
from contacts.models import ContactModel
from contacts import todos

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get('/', response_model=list[ContactResponseSchema])
async def root(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),db = Depends(get_database)) -> list[ContactResponseSchema]:
    contacts = await todos.get_contacts(limit, offset, db)
    return contacts

