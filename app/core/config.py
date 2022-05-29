import secrets
from typing import Optional, Dict, Any
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = "Incedo"
    SERVER_HOST: AnyHttpUrl = "http://0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_URL: str = f"{SERVER_HOST}:{SERVER_PORT}"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # User
    DEFAULT_AVATAR: str = f"{SERVER_URL}/static/images/avatars/default.png"
    FIRST_USER_USERNAME: str
    FIRST_USER_EMAIL: str
    FIRST_USER_PASSWORD: str

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    class Config:
        env_file = ".env"


settings = Settings()
