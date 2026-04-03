import os
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("day1_logger")
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler = logging.FileHandler(
        "logs/agent_logs.log",
        mode="a",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger