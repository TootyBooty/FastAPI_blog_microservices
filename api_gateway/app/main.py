from api.routes.auth import auth_router
from api.routes.blog import blog_router
from api.routes.service import service_router
from api.routes.user import user_router
from fastapi import APIRouter
from fastapi import FastAPI

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(auth_router, prefix="/login", tags=["auth"])
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(blog_router, prefix="/blog", tags=["blog"])
main_api_router.include_router(service_router, tags=["service"])


app.include_router(main_api_router)
