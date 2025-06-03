from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL : str
    PORT : int
    ENVIRONMENT : str = 'dev'



    class Config:
        env_file = SettingsConfigDict(
            env_file='.env',
            env_file_encoding='utf-8'
        )

