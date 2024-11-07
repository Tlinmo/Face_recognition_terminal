from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from loguru import logger


from app.log import configure_logging
from app.repository.dependencies import get_db_session
from app.repository.auth_repository import UserRepository
from app.services.auth.auth import AuthService
from app.services.auth.users import User
from app.services.auth.exceptions import AuthUsernameError
from app.web.api.auth import schema

configure_logging()

router = APIRouter()


@router.post("/create", status_code=201)
async def register(
    _user: schema.UserCreate, session: AsyncSession = Depends(get_db_session)
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
        return "Не получилось"


@router.post("/login")
async def authentication(
    _user: schema.UserCreate, session: AsyncSession = Depends(get_db_session)
) -> str:
    logger.debug("Авторизация пользователя")
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    token = await auth.authentication(username=_user.username, password=_user.password)
    if token:
        return token
    else:
        return 'Не получилось'


# Я шел по цепочке от репозитория до веб-апи ради этого, и я всё больше убеждаюсь что ему тут не место
# Но мне лень делать новый модуль для одной функции
@router.post("/list", response_model=List[schema.User])
async def lst(
    offset: int = 0, limit:int = 10, session: AsyncSession = Depends(get_db_session)
) -> List[User]:
    logger.debug("Получаем список пользователей")
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    users = await auth.lst(offset=offset, limit=limit)
    return users

@router.post("/user{id_:str}", response_model=schema.User)
async def show(
    id_: UUID, session: AsyncSession = Depends(get_db_session)
) -> User:
    logger.debug("Получаем пользователя")
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    users = await auth.show(id_=id_)
    return users



@router.put("/update", status_code=204)
async def update(
    _user: schema.UpdateUser, session: AsyncSession = Depends(get_db_session)):
    logger.debug("Обновляем пользователя")
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    user = User(id=_user.id, username=_user.username, embeddings=_user.embeddings)

    await auth.update(user)
