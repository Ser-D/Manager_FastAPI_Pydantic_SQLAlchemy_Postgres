import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.routes import router
from src.database.db_postgresql import get_database

app = FastAPI()

app.include_router(router)


@app.get('/')
def index():
    return {'message': 'My application'}


@app.get('/healthchecker')
async def healthchecker(db: AsyncSession = Depends(get_database)):
    try:
        result = await db.execute(text('Select 1'))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {'message': 'Welcome to FastAPI'}
    except Exception:
        raise HTTPException(status_code=500, detail='Error connecting to the database')

if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='localhost', port=8000, reload=True
        )