import logging
import re
import sys


class ConsoleFormatter(logging.Formatter):
    TIME = "\x1b[38;5;245m"  # Dim grey
    LEVEL = "\x1b[1;36m"  # Bold cyan
    NAME = "\x1b[1;35m"  # Bold magenta
    THREAD = "\x1b[38;5;109m"  # Muted blue/cyan

    RED = "\x1b[1;31m"  # Bold red
    BOLD_WHITE = "\x1b[1;37m"  # Bright white
    RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = record.levelname
        name = record.name
        msg = record.getMessage()

        # Handle indentation for msg
        msg = "\n      ".join(msg.split("\n"))

        time_str = f"{self.TIME}{time}{self.RESET}"
        level_str = f"{self.LEVEL}{level:<8}{self.RESET}"
        name_str = f"{self.NAME}{name.upper():<20}{self.RESET}"
        end_str = f" {self.TIME}>>{self.RESET}"
        msg_str = re.sub(
            r"\*(.*?)\*",
            lambda m: f"{self.BOLD_WHITE}{m.group(1)}{self.RESET}",
            msg
        )

        return (
            f"{time_str} {level_str} {name_str} {end_str}\n"
            f"      {msg_str}"
        )


def load_logger(debug: bool) -> logging.Logger:
    logger = logging.getLogger()

    if debug:
        logger.setLevel(logging.DEBUG)

    else:
        logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ConsoleFormatter())

    logging.getLogger("PIL").setLevel(logging.WARNING)

    logger.handlers.clear()
    logger.addHandler(console_handler)

    return logger