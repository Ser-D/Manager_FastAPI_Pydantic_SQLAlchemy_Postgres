import re
from ipaddress import ip_address
from typing import Callable

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.routes import router as cont_routers
from src.database.db_postgresql import get_database
from src.users.routes import router as users_routers
from src.users.routes_user import router as user_routers
from src.conf.config import config

app = FastAPI()

origins = ["http://localhost:8000",
           "http://127.0.0.1:8000"]

banned_ips = [
    ip_address("192.168.1.1"),
    ip_address("192.168.1.2",),
    # ip_address("127.0.0.1",)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST ...
    allow_headers=["*"],
)


# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


user_agent_ban_list = [r"Googlebot", r"Python-urllib"]


# @app.middleware("http")
# async def user_agent_ban_middleware(request: Request, call_next: Callable):
#     print(request.headers.get("Authorization"))
#     user_agent = request.headers.get("user-agent")
#     print(user_agent)
#     for ban_pattern in user_agent_ban_list:
#         if re.search(ban_pattern, user_agent):
#             return JSONResponse(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 content={"detail": "You are banned"},
#             )
#     response = await call_next(request)
#     return response


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
