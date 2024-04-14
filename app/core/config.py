from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Banner management"
    app_version: str = "0.1.0"
    database_url: str = "postgresql://postgres:postgres@5432:5432/postgres"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
