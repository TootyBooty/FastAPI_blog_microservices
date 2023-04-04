from fastapi import FastAPI, APIRouter, Depends

from routes import blog_router
from depends import verify_token

app = FastAPI(dependencies=[Depends(verify_token)])


@app.get('/')
def ping():
    return {'success': True}

main_api_router = APIRouter()
main_api_router.include_router(blog_router, prefix='/blog')

app.include_router(main_api_router)
