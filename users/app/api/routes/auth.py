from api.depends import get_user_repository
from api.schemas import UserInForLogin
from api.schemas import UserOutForLogin
from core.security import verify_password
from db.repositories import UserRepository
from exceptions import CredentialsException
from fastapi import APIRouter
from fastapi import Depends

auth_router = APIRouter()


@auth_router.post("/token", response_model=UserOutForLogin)
async def login_for_token(
    login_data: UserInForLogin, repo: UserRepository = Depends(get_user_repository)
):
    user = await repo.get_user_by_email(login_data.email)
    if user is None:
        raise CredentialsException

    if not verify_password(login_data.password, user.password):
        raise CredentialsException

    return UserOutForLogin(email=user.email, roles=user.roles)
