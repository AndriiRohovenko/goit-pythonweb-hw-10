import os
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class Config:
    DB_URL = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    JWT_SECRET = SECRET_KEY
    JWT_ALGORITHM = ALGORITHM
    JWT_EXPIRATION_SECONDS = 3600


config = Config()
os.environ["DB_URL"] = config.DB_URL
