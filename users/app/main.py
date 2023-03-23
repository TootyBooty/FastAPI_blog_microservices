from fastapi import FastAPI, APIRouter

from api.routes.user import user_router

app = FastAPI()


main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix='/user')


@main_api_router.get('/')
def ping():
    return {'success': True}


app.include_router(main_api_router)
