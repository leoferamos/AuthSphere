from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str
    DB_SCHEMA: str | None = None  # Optional schema for MySQL
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
