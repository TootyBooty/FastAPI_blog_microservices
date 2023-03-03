from fastapi import FastAPI, APIRouter

from routes import blog_router

app = FastAPI()


@app.get('/')
def ping():
    return {'success': True}

main_api_router = APIRouter()
main_api_router.include_router(blog_router)

app.include_router(main_api_router)
