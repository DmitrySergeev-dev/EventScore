from pathlib import Path

from pydantic import BaseModel
from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8006


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    scores: str = "/scores"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class RedisConfig(BaseModel):
    url: RedisDsn


class DBConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ENV_PATH.joinpath(".env.template"),
            ENV_PATH.joinpath(".env")
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SCORE_MAKER_CONFIG__"
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    redis: RedisConfig
    db: DBConfig


settings = Settings()
