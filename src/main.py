import uvicorn
import fastapi

import users.routes

user_api = fastapi.FastAPI()

user_api.include_router(users.routes.router)

if __name__ == '__main__':
    uvicorn.run(
        'main:user_api', host='0.0.0.0', port=8000, reload=True
        )