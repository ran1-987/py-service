from pathlib import Path

from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    uri: str = ""
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    mailgun_api_key: str = ""
    mailgun_domain: str = ""
    mailgun_from_email: str = "rakeshranjan.oracle@gmail.com"

    model_config = {
        "env_file": ROOT_DIR / ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
