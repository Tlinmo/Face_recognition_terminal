from typing import List
from abc import ABC, abstractmethod
import uuid

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from log import configure_logging
from app.services.auth.users import User
from app.repository.models.users import User as db_User
from app.repository.exceptions import UsernameError

configure_logging()


class IUserRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__()

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def get(
        self,
        id_: uuid.UUID | None = None,
        username: str | None = None,
    ) -> User:
        pass

    @abstractmethod
    async def list(self, limit: int = 10) -> List[User]:
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID, user: User):
        pass

    @abstractmethod
    async def save(self):
        pass


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add(self, user: User) -> User:
        db_user = db_User(
            username=user.username,
            hashed_password=user.hashed_password,
            is_superuser=user.is_superuser,
        )
        self.session.add(db_user)
        await self.save()
        _user = User(**db_user.dict())
        return _user

    async def get(
        self,
        id_: uuid.UUID | None = None,
        username: str | None = None,
    ) -> User:
        sql = select(db_User)

        if id_:
            sql = select(db_User).filter(db_User.id == id)
        if username:
            sql = select(db_User).filter(db_User.username == username)

        user = await self.session.execute(sql)
        user = user.scalars().one_or_none()

        if user:
            return User(**user.dict())

    async def list(self, limit: int = 10) -> List[User]:
        return super().list(limit)

    async def update(self, id_: uuid.UUID, user: User):
        return super().update(id_, user)

    async def save(self):
        try:
            logger.debug("Производится commit")
            await self.session.commit()
        except IntegrityError as error:
            logger.error(error)
            raise UsernameError("Username уже занят")
        except Exception as error:
            logger.error(error)
            await self.session.rollback()
