import random
import string
from datetime import datetime, timezone, timedelta
from time import sleep
from loggers import logger, tz_jkt
import requests


def generate_random_alphanumeric_string(length: int = 13) -> str:
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_string

def generate_random_number(length: int = 7) -> int:
    random_string = ''.join(random.choices(string.digits, k=length))
    return random_string

def retry_wrapper(max_retries: int = 5, delay: int = 10):
    def outer(func):
        def inner(*args, **kwargs):
            for i in range(1, max_retries + 1):
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as err:
                    logger.error(err)
                    logger.warning(f'Retrying... ({i} / {max_retries})')
                    sleep(delay)
            msg = 'Retry attempt limit reached. Task aborted.'
            logger.error(msg)
            raise Exception(msg)
        return inner
    return outer

retry = retry_wrapper(5, 10)
get_with_retry = retry(requests.get)