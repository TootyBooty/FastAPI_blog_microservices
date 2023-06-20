from api.depends import verify_token
from api.routes.blog import blog_router
from api.routes.service import service_router
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI


app = FastAPI(dependencies=[Depends(verify_token)])


main_api_router = APIRouter()
main_api_router.include_router(blog_router, prefix="/blog", tags=["blog"])
main_api_router.include_router(service_router, tags=["service"])


app.include_router(main_api_router)
