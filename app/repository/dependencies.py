from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from loguru import logger

from log import configure_logging

configure_logging()


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        logger.debug("Выдается сессия")
        yield session
        # logger.debug("Производится  commit")
        # await session.commit()
    except Exception as error:
        logger.error(error)
        await session.rollback()
    finally:
        await session.close()


# class UnitOfWork:
#     def __init__(self) -> None:
#         self.session_maker = sessionmaker(
#             bind=create_async_engine()
#         )

#     def __enter__(self):
#         self.session = self.session_maker()
#         return self

#     def __exit__(self, exc_type, exc_val, traceback):
#         if exc_type is not None:
#             self.rollback()
#         self.session.close()

#     def commit(self):
#         self.session.commit()

#     def rollback(self):
#         self.session.rollback()
