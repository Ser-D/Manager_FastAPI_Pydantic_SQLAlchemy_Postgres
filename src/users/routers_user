from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter

from src.database.db_postgresql import get_database
from src.users import repository 
from src.users.schemas import UserSchema, TokenSchema, UserResponseSchema, LogoutResponse, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from src.contacts.models import User

router = APIRouter(prefix='/user', tags=['user'])

@router.get(
    "/me",
    response_model=UserResponseSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user