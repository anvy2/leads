from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "test"
    app_env: str = "local"
    database_conn_uri: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres"
    model_config = SettingsConfigDict(env_file=Path(Path(__file__).parent.parent.resolve(), ".env"))


settings = Settings()
