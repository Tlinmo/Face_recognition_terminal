from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from loguru import logger


from log import configure_logging
from app.repository.dependencies import get_db_session
from app.repository.auth_repository import UserRepository
from app.services.auth.auth import AuthService
from app.services.auth.users import User
from app.web.api.user import schema

configure_logging()

router = APIRouter()


@router.get("/", response_model=List[schema.User], status_code=200)
async def list_users(
    offset: int = 0, limit:int = 10, session: AsyncSession = Depends(get_db_session)
) -> List[User]:
    """Получение списка с дынными о пользователях"""
    
    logger.debug("Получаем список пользователей")
    
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)
    
    users = await auth.lst(offset=offset, limit=limit)
    
    return users

@router.get("/{id_:str}", response_model=schema.User, status_code=200)
async def user_info(
    id_: UUID, session: AsyncSession = Depends(get_db_session)
) -> User:
    """Получение дынных о пользователе"""
    
    logger.debug(f"Получаем данные пользователя c id {id_}")
    
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)

    users = await auth.show(id_=id_)
    return users

@router.put("/{id_:str}", status_code=204)
async def update(
    id_:UUID , _user: schema.UpdateUser, session: AsyncSession = Depends(get_db_session)):
    """Изменение данных о пользователе"""
    
    logger.debug(f"Обновляем данные пользователя c id {id_}")
    
    repo = UserRepository(session=session)
    auth = AuthService(user_repository=repo)
    
    user = User(id=id_, username=_user.username, embeddings=_user.embeddings)
    
    await auth.update(user)