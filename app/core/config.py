import os

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    BASE_REPO_PATH: str = "/tmp/repos"

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

settings = Settings()
