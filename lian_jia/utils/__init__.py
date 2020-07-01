import random
from pathlib import Path
from typing import Any

from lian_jia.config import USER_AGENT


def get_user_agent():
    return random.choice(USER_AGENT)


def dump(obj: Any, path: Path):
    if isinstance(obj, (list, dict, tuple)):
        import json

        res = json.dumps(obj)
        file_type = "w"
    else:
        import pickle

        res = pickle.dumps(obj)
        file_type = "wb"
    with open(path, file_type) as f:
        f.write(res)
