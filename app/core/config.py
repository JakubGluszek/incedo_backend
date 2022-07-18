import os
from typing import Any, Dict, Optional

import dotenv
from pydantic import BaseSettings, EmailStr, Field, validator

dotenv.load_dotenv()


class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = "Incedo"
    DEVELOPMENT: bool = os.getenv("DEVELOPMENT", False)

    HOST: str = os.getenv("HOST")
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST")

    # Database
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)

    # User
    DEFAULT_AVATAR: str = f"{HOST}/static/images/avatars/default.png"
    FIRST_USER_EMAIL: EmailStr = os.getenv("FIRST_USER_EMAIL")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SIGN_IN_TOKEN_EXPIRE_HOURS: int = 2

    # Mail
    SMTP_TLS: bool = True
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: EmailStr = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME", None)
    EMAIL_TEMPLATES_DIR: str = "./app/email-templates/"

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+pymysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}/{values.get('DB_NAME')}"

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = os.getenv("SECRET_KEY")
    authjwt_token_location = {"cookies", "headers"}
    authjwt_access_token_expires: int = 60 * 60  # seconds
    authjwt_cookie_csrf_protect: bool = os.getenv("authjwt_cookie_csrf_protect")
    authjwt_cookie_secure: bool = os.getenv("authjwt_cookie_secure")
    authjwt_cookie_domain: str = os.getenv("authjwt_cookie_domain")

    class Config:
        env_file = ".env"


settings = Settings()
