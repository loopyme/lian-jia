import time
import warnings

import requests

from lian_jia.config import INTERVAL
from lian_jia.utils import get_user_agent

LAST_REQUEST_TIME = 0


def get(url: str):
    check_interval()
    response = requests.get(url, headers={"User-Agent": get_user_agent()})

    if (status := response.status_code) != 200:
        warnings.warn(f"Request to {url} return status-{status}")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Get {url}")
    return response.text


def check_interval():
    global LAST_REQUEST_TIME
    if not (now := time.time()) > LAST_REQUEST_TIME + INTERVAL:
        time.sleep(LAST_REQUEST_TIME + INTERVAL - now)
    LAST_REQUEST_TIME = time.time()
