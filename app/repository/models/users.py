import json
import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.types import TypeDecorator, CHAR, Text
from loguru import logger

from app.repository.base import Base
from app.log import configure_logging

configure_logging()


class UUIDType(TypeDecorator):
    """Custom UUID type for SQLite."""

    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    is_superuser = Column(Boolean, default=False)
    embedding = Column(Text)

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "is_superuser": self.is_superuser,
            # "embedding": self.embedding, # верни когда перейдешь на postgresql
        }

    def set_embedding(self, values):
        """Сериализация массива в строку JSON."""
        logger.debug("Сериализация embedding в строку")
        self.embedding = json.dumps(values)
        logger.debug(
            f"self.embedding: {self.embedding}, json.dumps(values): {json.dumps(values)}"
        )

    def get_embedding(self) -> list:
        """Десериализация строки JSON в массив."""
        if self.embedding:
            logger.debug("Десериализация строки JSON в массив")
            logger.debug(
                f"self.embedding: {self.embedding}, json.loads(self.embedding): {json.loads(self.embedding)}"
            )
            return json.loads(self.embedding)

        return []
