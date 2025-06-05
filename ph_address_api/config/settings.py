from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

"""
Imported the required modules, such as the BaseSettings, SettingsConfigDict in pydantic_settings. 
Create a object called Settings and inherit all attributes and functions of BaseSetting.

"""
class Settings(BaseSettings):

    #Database URL of your db
    DB_URL : str
    #local port number.Used in uvicorn server to custom the ports
    PORT : int
    #In normal this is dev, it means the db used is the sql lite,
    # otherwise store in the specific database, such us the online db or other platforms.
    ENVIRONMENT : str = 'prod'

    #Configuration of the settings
    class Config:
        env_file = SettingsConfigDict(
            env_file='.env',
            env_file_encoding='utf-8'
        )

