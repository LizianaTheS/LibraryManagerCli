from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    secret_key: str = Field(alias="SECRET_KEY")
    debug: bool = Field(alias="DEBUG")
    jwt_secret: str = Field(alias="JWT_SECRET")
    log_level: str=Field(alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        populate_by_name = True  # allows using field names as well

settings = Settings()
