import uvicorn
import fastapi

from contacts.routes import router

user_api = fastapi.FastAPI()

user_api.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:user_api', host='localhost', port=8000, reload=True
        )