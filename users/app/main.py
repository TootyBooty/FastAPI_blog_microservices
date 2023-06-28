from api.depends import verify_token
from api.routes.auth import auth_router
from api.routes.service import service_router
from api.routes.user import user_router
from db.repositories import UserRepository
from db.session import async_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI


app = FastAPI(dependencies=[Depends(verify_token)])


@app.on_event("startup")
async def create_superadmin():
    session = async_session()
    repo = UserRepository(session)
    await repo.create_superadmin()


main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])

app.include_router(main_api_router)
