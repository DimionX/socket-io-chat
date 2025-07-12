import json
import os
from functools import lru_cache
from os import path

from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()


class Config:
    # [APP]
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEFAULT_SERVER_URL = f"{HOST}:{PORT}"
    SERVER_URL = os.getenv("SERVER_URL", DEFAULT_SERVER_URL)
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # [TOTP Auth]
    TOTP_SECRET = os.getenv("TOTP_SECRET")
    TOTP_USER = os.getenv("TOTP_USER")
    TOTP_ISSUER_NAME = os.getenv("TOTP_ISSUER_NAME")
    STORAGE_LIMITER = os.getenv("STORAGE_LIMITER")
    TOTP_USED_PATH = os.getenv("TOTP_USED_PATH")

    # [Telegram]
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_LOG_LEVEL = os.getenv("TELEGRAM_LOG_LEVEL", "ERROR")

    @classmethod
    def get_limiter(cls, app: Flask) -> Limiter:
        return Limiter(app=app, key_func=get_remote_address, strategy="fixed-window", storage_uri=cls.STORAGE_LIMITER)

    @classmethod
    @lru_cache()
    def get_build(cls) -> str:
        current_dir = path.dirname(path.abspath(__file__))
        build_path = path.join(current_dir, "static", "build.json")

        with open(build_path, "r") as f:
            data = json.load(f)

        return data["version"]
