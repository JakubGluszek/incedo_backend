import os
import dotenv
from typing import Optional, Dict, Any
from pydantic import (
    BaseSettings,
    EmailStr,
    PostgresDsn,
    validator,
)


dotenv.load_dotenv()


class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = "Incedo"
    DEBUG: bool = False
    BACKEND_HOST: str = "http://0.0.0.0:8000"
    FRONTEND_HOST: str = "http://0.0.0.0:3000"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v.replace("postgres://", "postgresql://")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # User
    DEFAULT_AVATAR: str = f"{BACKEND_HOST}/static/images/avatars/default.png"
    FIRST_USER_USERNAME: str
    FIRST_USER_EMAIL: str

    # Security
    SECRET_KEY: str
    SIGN_IN_TOKEN_EXPIRE_HOURS: int = 2

    # Mail
    SMTP_TLS: bool = True
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: EmailStr
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_TEMPLATES_DIR: str = "./app/email-templates/"

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = os.getenv("SECRET_KEY")
    authjwt_token_location = {"cookies"}
    authjwt_access_token_expires: int = 60 * 60  # seconds
    authjwt_cookie_csrf_protect: bool
    authjwt_cookie_secure: bool
    authjwt_cookie_domain: str

    class Config:
        env_file = ".env"


settings = Settings()
