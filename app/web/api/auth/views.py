from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from loguru import logger


from log import configure_logging
from app.repository.dependencies import get_db_session
from app.repository.auth_repository import UserRepository
from app.services.auth.auth import AuthService
from app.services.auth.users import User
from app.services.auth.exceptions import AuthUsernameError
from app.web.api.auth import schema

configure_logging()

router = APIRouter()


@router.post("/create")
async def register(
    _user: schema.AuthCreate, session: AsyncSession = Depends(get_db_session)
) -> str:
    logger.debug("Создание пользователя")

    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)
    user = User(
        username=_user.username, hashed_password=User.hash_password(_user.password)
    )
    try:
        token = await auth.register(user)
        return token
    except AuthUsernameError:
        logger.debug(
            "Создание пользователя не получилось, веб апишка это видит и может дефать"
        )
        return "Хуй"


@router.post("/login")
async def authentication(
    _user: schema.AuthCreate, session: AsyncSession = Depends(get_db_session)
) -> str:
    logger.debug("Авторизация пользователя")
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    token = await auth.authentication(username=_user.username, password=_user.password)
    if token:
        return token
    else:
        return 'Хоуй'
