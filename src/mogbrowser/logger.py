import logging
import sys


class ConsoleFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLOURS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[94m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[1;31m",
    }

    def format(self, record: logging.LogRecord) -> str:
        colour = self.COLOURS.get(record.levelno, self.RESET)

        record_copy = logging.makeLogRecord(record.__dict__.copy())
        record_copy.levelname = f"{colour}{record.levelname:<8}{self.RESET}"
        record_copy.name = f"{record.name.upper():<10}"

        return super().format(record_copy)


def load_logger(debug: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if debug else logging.INFO)

    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ConsoleFormatter(
            fmt="%(asctime)s │ %(levelname)s │ %(name)s │ %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    root.addHandler(handler)