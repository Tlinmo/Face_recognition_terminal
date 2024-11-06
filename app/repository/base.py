from sqlalchemy.orm import DeclarativeBase

from auth_service.repository.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
