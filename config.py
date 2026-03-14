import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "postgresql://estoque_user:estoque_pass@localhost:5433/estoque_db",
    )
