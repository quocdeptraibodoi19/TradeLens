from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    alpaca_app_client_id: str
    alpaca_app_client_secret: str
    fernet: str
    app_db_user: str
    app_db_password: str
    app_db_name: str
    app_db_host: str
    app_db_port: str
    session_secret_key: str
    frontend_url: str = "http://localhost:5173"

    ch_host: str
    ch_port: int = 8123
    ch_user: str
    ch_password: str

    lz_schema: str = "landing_zone"

    @computed_field
    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql://{self.app_db_user}:{self.app_db_password}"
            f"@{self.app_db_host}:{self.app_db_port}/{self.app_db_name}"
        )

    @computed_field
    @property
    def clickhouse_url(self) -> str:
        return (
            f"clickhouse+connect://{self.ch_user}:{self.ch_password}"
            f"@{self.ch_host}:{self.ch_port}"
        )


settings = Settings()
