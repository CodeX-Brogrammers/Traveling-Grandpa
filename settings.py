from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    path: str = Field("", alias="URL_PATH")
    port: int = Field(3000, alias="PORT")
    host: str = Field("localhost")

    mongodb_url: str = Field("mongo://127.0.0.1:27017", alias="MONGODB_URL")


settings = Settings()
