import logging
from config import LOG_FILE, LOG_LEVEL

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), "INFO"))

    if not logger.handlers:
        fh = logging.FileHandler(LOG_FILE)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
