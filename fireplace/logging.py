import logging
from .i18n import _ as translate


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter(
            "[%(name)s.%(module)s]: %(message)s", datefmt="%H:%M:%S"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger


# Translation-aware logging function
def log_info(key, **kwargs):
    """
    Log an info message with translation support.

    Args:
        key: Translation key
        **kwargs: Format arguments for the message
    """
    message = translate(key, **kwargs)
    log.info(message)


log = get_logger("fireplace")
