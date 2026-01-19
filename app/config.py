from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    TEEINBLUE_API_KEY: str
    TEEINBLUE_API_URL: str = "https://api.teeinblue.com/openapi/v1"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "teeinblue"

    # Redis
    REDIS_URL: Optional[str] = None

    @property
    def DATABASE_URL(self) -> str:
        # Construct Postgres URL from parts
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore" # Ignore extra fields in .env

settings = Settings()
