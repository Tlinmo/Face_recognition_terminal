from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import List
from uuid import UUID

# from cryptography.hazmat.primitives import serialization
# import jwt
from loguru import logger
from app.repository.exceptions import UsernameError

from app.repository.auth_repository import IUserRepository
from app.services.auth.users import User
from app.services.auth.exceptions import AuthUsernameError
from log import configure_logging
from settings import APP_ROOT

configure_logging()


# def generate_jwt(id_:UUID) -> str:
#     now = datetime.now(UTC)
#     payload = {
#         "iss": "https://auth.example.com/",
#         "sub": id_,
#         "aud": "http://127.0.0.1:8000/",
#         "iat": now.timestamp(),
#         "exp": (now + timedelta(hours=24)).timestamp(),
#         "scope": "bopenid",
#     }

#     private_key_text = (APP_ROOT / "ssl" / "private_key.pem").read_text()
#     private_key = serialization.load_pem_private_key(
#         private_key_text.encode(), password=None
#     )

#     return jwt.encode(payload=payload, key=private_key, algorithm="RS256")


class AuthService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    async def register(self, user: User) -> str:
        try:
            _user = await self.user_repository.add(user=user)
            logger.debug(_user.__dict__)

            # Если id к этому моменту нет, сработает исключение на уровне репозитория
            if _user.id:
                # return generate_jwt(id_=_user.id)
                return "Всё збс"
            else:
                return "Кажется всё пошло по ***** чекай логи"
            
        except UsernameError as error:
            logger.debug(error)
            raise AuthUsernameError()

    # Тут по хорошему тоже тру кач ебнуть, что бы глаз радовался и проверочки  можно было делать разные
    async def authentication(self, username:str, password:str) -> str:
        _user = await self.user_repository.get(username=username)
        if _user.check_password(password):
            return "тут типа токен? а зач?"
        return "password не верный"
            
    # Это тут вообще не к месту но рефакторить будем потом Гы)
    async def lst(self, offset:int, limit: int) -> List[User]:
        _users = await self.user_repository.list(offset=offset, limit=limit)
        return _users
    
    async def show(self, id_: UUID) -> User:
        _user = await self.user_repository.get(id_=id_)
        return _user

    
    async def update(self, user: User):
        _users = await self.user_repository.update(user=user)
        return _users
