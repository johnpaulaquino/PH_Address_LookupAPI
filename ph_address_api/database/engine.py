from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from ph_address_api.config.settings import Settings
from pathlib import Path
settings = Settings()

'''
@:var engine
    - This engine contains the url for db_services, to make a connection in db
'''
#from absolute path, then go down two directories to find the sql db
sql_lite = Path(__file__).resolve().parent.parent.parent / 'dev.db'

#if the environment is == dev, then the data will insert in sqlite, otherwise in real db.
if settings.ENVIRONMENT == 'dev':
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{sql_lite}",
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(
    settings.DB_URL
    )

# Create a session factory
LocalSession = sessionmaker(
    class_=AsyncSession, bind=engine,
    autoflush=False,
    expire_on_commit=False
)


@asynccontextmanager
async def create_session() -> AsyncSession:
    """
           Asynchronous context manager for managing db_services sessions.

           This function provides a safe way to manage db_services sessions in an asynchronous application. It ensures that
           sessions are properly created, errors are handled, and sessions are closed after use.

           Yields:
               AsyncSession: An instance of the db_services session to perform db_services operations.

           Raises:
               SQLAlchemyError: If a db_services-related error occurs, it is logged and re-raised for further handling.
           """
    async with LocalSession() as session:
        try:
            yield session
        except Exception as e:
            print(f'An error occurred {e}!')
            await session.rollback()




