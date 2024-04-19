from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from src.database.db_postgresql import get_database
from src.users import repository 
from src.users.schemas import UserSchema, TokenSchema, UserResponseSchema, LogoutResponse, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from  src.conf import messages


router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, bt: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_database)):
    exist_user = await repository.get_user_by_email(body.email, db)
    if exist_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_database)):
    user = await repository.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_CREDENTIALS)
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.NOT_CONFIRM)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_CREDENTIALS)
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
                        db: AsyncSession = Depends(get_database)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository.get_user_by_email(email, db)
    
    if user.refresh_token != token:
        await repository.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_CREDENTIALS)
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_202_ACCEPTED)
async def logout(
        user=Depends(auth_service.get_current_user),
        db=Depends(get_database),
):
    user.refresh_token = None
    await db.commit()

    return {"result": "Logout success"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_database)):
    email = await auth_service.get_email_from_token(token)
    user = await repository.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_database)):
    user = await repository.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}


@router.get('/{username}')
async def request_email(username: str, response: Response, db: AsyncSession = Depends(get_database)):
    print('--------------------------------')
    print(f'{username} зберігаємо що він відкрив email в БД')
    print('--------------------------------')
    return FileResponse("src/static/open_check.png", media_type="image/png", content_disposition_type="inline")