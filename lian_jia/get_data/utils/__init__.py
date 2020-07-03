import json
import random
from pathlib import Path
from typing import Any

import pandas as pd

from lian_jia.config import DATA_DIR, HOUSE_DISTRICT_DICT
from lian_jia.get_data.config import USER_AGENT


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


def to_csv():
    chengjiao_data = []
    ershoufang_data = []
    for hs, name in HOUSE_DISTRICT_DICT.items():
        with open(DATA_DIR / "house_info" / "chengjiao" / f"{hs}.json", 'r') as f:
            house_dicts = json.loads(f.read())
            for dic in house_dicts:
                dic['地区'] = name
            chengjiao_data += house_dicts
        with open(DATA_DIR / "house_info" / "ershoufang" / f"{hs}.json", 'r') as f:
            house_dicts = json.loads(f.read())
            for dic in house_dicts:
                dic['地区'] = name
            ershoufang_data += house_dicts
    pd.DataFrame(chengjiao_data).to_csv(DATA_DIR / "house_info" / "chengjiao.csv")
    pd.DataFrame(ershoufang_data).to_csv(DATA_DIR / "house_info" / "ershoufang.csv")


def mkdir_res():
    if not DATA_DIR.is_dir():
        raise NotADirectoryError(f"{DATA_DIR} is not a dir")

    (DATA_DIR / "house_info" / "chengjiao").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "house_info" / "ershoufang").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "house_url" / "chengjiao").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "house_info" / "ershoufang").mkdir(parents=True, exist_ok=True)
