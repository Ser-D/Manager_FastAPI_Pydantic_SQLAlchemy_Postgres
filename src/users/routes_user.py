import pickle

import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, Response, UploadFile, File
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
from src.conf.config import config

router = APIRouter(prefix='/user', tags=['user'])

cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponseSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router.patch(
    "/avatar",
    response_model=UserResponseSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_database),
):
    public_id = f"contacts_web/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repository.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
