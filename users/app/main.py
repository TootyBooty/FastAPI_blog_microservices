from fastapi import FastAPI, APIRouter


app = FastAPI()


main_api_router = APIRouter(prefix='/users')

@main_api_router.get('/')
def ping():
    return {'success': True}


app.include_router(main_api_router)
