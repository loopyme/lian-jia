from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from lian_jia.config import HOUSE_DISTRICT_DICT, DATA_DIR
from lian_jia.get_data.config import WORKER
from lian_jia.get_data.crawler.house_info import get_ershoufang_house_info, get_chengjiao_house_info
from lian_jia.get_data.crawler.house_url import get_chengjiao_house_url, get_ershoufang_house_url
from lian_jia.get_data.utils import mkdir_res, to_csv


def get_data():
    executor = ThreadPoolExecutor(max_workers=WORKER)

    # get the res dir ready
    mkdir_res()

    # get url
    list(
        as_completed(
            executor.submit(get_chengjiao_house_url, ),
            executor.submit(get_ershoufang_house_url, ),
        )
    )

    # get ershoufang info
    list(
        as_completed(
            executor.submit(get_ershoufang_house_info, hs)
            for hs, name in HOUSE_DISTRICT_DICT.items()
            if not (DATA_DIR / "house_info" / "ershoufang" / f"{hs}.json").is_file()
        )
    )

    # get chengjiao info
    list(
        as_completed(
            executor.submit(get_chengjiao_house_info, hs)
            for hs, name in HOUSE_DISTRICT_DICT.items()
            if not (DATA_DIR / "house_info" / "chengjiao" / f"{hs}.json").is_file()
        )
    )

    # save to csv
    to_csv()
