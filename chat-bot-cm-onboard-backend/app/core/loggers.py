import logging
import sys

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)')

handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)