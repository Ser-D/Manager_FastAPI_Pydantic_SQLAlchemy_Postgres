import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.routes import router as cont_routers
from src.database.db_postgresql import get_database
from src.users.routes import router as users_routers
from src.users.routes_user import router as user_routers
from src.conf.config import config

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(cont_routers)
app.include_router(users_routers)
app.include_router(user_routers)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)


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
