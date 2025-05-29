from contextlib import asynccontextmanager
from ph_address_api.config.settings import Settings


settings = Settings()
class AppUtility:

    @staticmethod
    @asynccontextmanager
    async def app_life_span(app):
        print(f'The Server is starting at port {settings.PORT}...')
        yield
        print(f'The Server is shutting down...')