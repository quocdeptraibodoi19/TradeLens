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

settings = Settings()
