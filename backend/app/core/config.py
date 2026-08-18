"""
Saari settings/secrets yaha rakhte hain (best practice - hardcode nahi karte).
.env file se values load hongi.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/complaints_db"

    # Model names
    EXTRACTION_MODEL: str = "openai/gpt-oss-20b"
    REASONING_MODEL: str = "openai/gpt-oss-120b"
    class Config:
        env_file = ".env"


settings = Settings()