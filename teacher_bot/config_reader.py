from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_uid: int
    admin_username: str
    admin_firstname: str
    admin_lastname: str
    max_message_length: int = Field(default=4096)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
config = Settings()



