import logging

from decouple import config

PATH_SAVE = config('PATH_SAVE', '')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
