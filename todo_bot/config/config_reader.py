from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()