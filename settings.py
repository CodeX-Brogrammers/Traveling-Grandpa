from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    path: str = Field("", alias="URL_PATH")
    port: int = Field(3000, alias="PORT")
    host: str = Field("localhost", alias="HOST")

    mongodb_url: str = Field("mongo://127.0.0.1:27017", alias="MONGODB_URL")
    redis_url: str = Field("redis://127.0.0.1:6379", alias="REDIS_URL")
    redis_enable: bool = Field(False, alias="REDIS_ENABLE")


settings = Settings()
