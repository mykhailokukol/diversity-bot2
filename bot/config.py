from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    TG_API_TOKEN = getenv("TG_API_TOKEN")
    MONGODB_CLIENT_URL = getenv("MONGODB_CLIENT_URL")


settings = Settings()
