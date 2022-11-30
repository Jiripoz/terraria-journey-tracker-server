import logging


class ColourFormatter(logging.Formatter):

    LEVEL_COLOURS = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]

    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


def setup_logger():
    logger = logging.getLogger("global")
    logger.setLevel(logging.INFO)

    # Pretty logger to stdout
    handler = logging.StreamHandler()
    handler.setFormatter(ColourFormatter())
    logger.addHandler(handler)
    return logger


def get_main_logger():
    return logging.getLogger("global")


def change_log_level(logger, level):
    logger.setLevel(level)


def make_main_logger_verbose(enable=False):
    logger = get_main_logger()
    if enable:
        change_log_level(logger, "DEBUG")
    else:
        change_log_level(logger, "INFO")