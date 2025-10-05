import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="EQ_DMBS.log"):
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] (%(name)s): %(message)s")
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    root.addHandler(logging.StreamHandler())
