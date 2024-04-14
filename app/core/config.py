from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Banner management"
    app_version: str = "0.1.0"
    database_url: str = "postgresql://postgres:postgres@5432:5432/postgres"
    secret: str = "SECRET"
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None
    first_superuser_role: str | None = 'admin'

    class Config:
        env_file = ".env"


settings = Settings()
