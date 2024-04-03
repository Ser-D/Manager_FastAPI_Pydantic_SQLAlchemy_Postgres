import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.routes import router as cont_routers
from src.database.db_postgresql import get_database
from src.users.routes import router as user_routers

app = FastAPI()

app.include_router(cont_routers)
app.include_router(user_routers)


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
