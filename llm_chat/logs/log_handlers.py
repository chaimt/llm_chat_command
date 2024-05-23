# Create a logger
import logging
from logging.handlers import RotatingFileHandler

from llm_chat.helper.app_utils import AppUtils


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a file handler and set the formatter
file_handler = RotatingFileHandler(f"{AppUtils().get_log_dir()}/log.txt", maxBytes=10000000, backupCount=20, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a console handler and set the formatter
# console_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False, markup=True)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def setup_log(log_level):
    console_handler.setLevel(level=log_level)
    for v in logging.Logger.manager.loggerDict.values():
        if type(v) == logging.Logger:
            if v.name.startswith("llm_chat.")  or v.name == "__main__":
                v.setLevel(level=log_level)
                v.removeHandler(file_handler)
                v.removeHandler(console_handler)
                v.addHandler(file_handler)
                if not v.name.startswith("llm_chat.logs.log_handlers"):
                    v.addHandler(console_handler)
