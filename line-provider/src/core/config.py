from pathlib import Path

from pydantic import BaseModel
from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8005


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ENV_PATH.joinpath(".env.template"),
            ENV_PATH.joinpath(".env")
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="LINE_PROVIDER_CONFIG__"
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
