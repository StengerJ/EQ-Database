import logging.config

def setup_logger(log_file="logs/EQ_DMBS.log"):
    logging.config.fileConfig('logger/logger.conf')

