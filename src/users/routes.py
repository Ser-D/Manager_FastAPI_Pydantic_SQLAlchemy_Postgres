import fastapi

import users.schemas as schemas

router = fastapi.APIRouter(prefix='/users', tags=['users'])

@router.get('/')
async def root() -> schemas.UserResponseSchema:
    return schemas.UserResponseSchema(
        id=1, 
        name='Angry',
        surname='Bird',
        email='example@gmail.com',
        birthday='1991.05.05',
        info='ups or not ups'
        )