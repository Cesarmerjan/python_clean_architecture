import logging
import logging.config

logging.config.fileConfig("src/logging.conf")

file_logger = logging.getLogger("file_logger")
