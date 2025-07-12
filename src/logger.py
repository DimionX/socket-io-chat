import json
import logging
from logging import LogRecord
from logging.handlers import RotatingFileHandler
from os import makedirs, path

import requests
from flask import Flask


class TelegramHandler(logging.Handler):
    TIMEOUT_TELEGRAM_BOT_SEC: int = 3

    def emit(self, record):
        try:
            from config import Config

            if not (Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID):
                return

            log_entry = self.format(record)
            requests.post(
                f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": Config.TELEGRAM_CHAT_ID,
                    "text": f"🚨 <b>{record.levelname}</b>\n<pre>{log_entry}</pre>",
                    "parse_mode": "HTML",
                },
                timeout=self.TIMEOUT_TELEGRAM_BOT_SEC,
            )
        except Exception as e:
            print(f"Failed to send log to Telegram: {e}")


class JsonFormatter(logging.Formatter):
    AVAILABLE_EXTRA_NAMES = {
        "ip",
        "user_agent",
        "code",
    }

    def format(self, record: LogRecord):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key in self.AVAILABLE_EXTRA_NAMES:
                log_record[key] = value

        return json.dumps(log_record, ensure_ascii=False)


def setup_logger(app_name: str = "app"):
    from config import Config

    logger = logging.getLogger(app_name)
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    current_dir = path.dirname(path.abspath(__file__))
    log_dir = path.join(current_dir, "logs")
    makedirs(log_dir, exist_ok=True)
    log_file = path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=5, encoding="utf-8")
    file_handler.setLevel(log_level)

    json_formatter = JsonFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(json_formatter)

    logger.addHandler(file_handler)

    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        telegram_log_level = getattr(logging, Config.TELEGRAM_LOG_LEVEL.upper(), logging.ERROR)

        telegram_handler = TelegramHandler()
        telegram_handler.setLevel(telegram_log_level)
        telegram_handler.setFormatter(json_formatter)
        logger.addHandler(telegram_handler)

    return logger


def init_logger(app: Flask):
    logger = setup_logger()

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    logging.getLogger("werkzeug").handlers = logger.handlers
    logging.getLogger("werkzeug").setLevel(logger.level)
