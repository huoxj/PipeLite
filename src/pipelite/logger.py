import logging
import sys

_default_fmt = "%(asctime)s-%(levelname)s [%(name)s]: %(message)s"
_default_datefmt = "%H:%M:%S"

logging.getLogger().handlers.clear()
logging.getLogger().propagate = False
logging.getLogger().setLevel(logging.INFO)

info = logging.info
warning = logging.warning
error = logging.error
debug = logging.debug

def get_logger(
    name: str,
    level: int = logging.INFO,
    propagate: bool = False,
    fmt: str = _default_fmt,
    filename: str | None = None,
    stream = sys.stdout
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate

    formatter = logging.Formatter(
        fmt=fmt,
        datefmt=_default_datefmt
    )

    if stream is not None:
        console_handler = logging.StreamHandler(stream)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if filename:
        file_handler = logging.FileHandler("./logs/" + filename, mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger