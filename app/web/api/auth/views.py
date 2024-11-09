from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger


from app.log import configure_logging
from app.repository.dependencies import get_db_session
from app.repository.auth_repository import UserRepository
from app.services.auth.auth import AuthService
from app.services.users.user import User
from app.services.auth.exceptions import AuthUsernameError, AuthPasswordError
from app.web.api.auth import schema

configure_logging()

router = APIRouter()


@router.post("/create", status_code=201)
async def register(
    _user: schema.UserCreate, session: AsyncSession = Depends(get_db_session)
) -> str:
    """Cоздание пользователя"""

    logger.debug("Создание пользователя")

    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)
    user = User(
        username=_user.username,
        hashed_password=User.hash_password(_user.password),
        embedding=_user.embedding,
    )
    try:
        token = await auth.register(user)
        return token
    except AuthUsernameError:
        raise HTTPException(status_code=409, detail="Такой пользователь уже есть")


@router.post("/login", status_code=200)
async def authentication(
    _user: schema.AuthUser, session: AsyncSession = Depends(get_db_session)
) -> str:
    """Авторизация пользователя"""
    logger.debug("Авторизация пользователя")

    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    try:
        token = await auth.authentication(username=_user.username, password=_user.password)
        return token
    except AuthPasswordError:
        raise HTTPException(status_code=401, detail="Пароль не верный")
    except AuthUsernameError:
        raise HTTPException(status_code=401, detail="Логин не верный")