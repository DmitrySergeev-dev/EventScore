from src.core.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "verbose_output": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_output": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "root": {
        "level": settings.log.level,
        "handlers": ["verbose_output"]
    },
}
