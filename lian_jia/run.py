from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from lian_jia.config import HOUSE_DISTRICT_DICT, RES_DIR, WORKER
from lian_jia.crawler.house_info import (
    get_ershoufang_house_info,
    get_chengjiao_house_info,
)
from lian_jia.crawler.house_url import get_chengjiao_house_url, get_ershoufang_house_url
from lian_jia.utils import to_csv


def craw():
    executor = ThreadPoolExecutor(max_workers=WORKER)

    list(
        as_completed(
            executor.submit(get_chengjiao_house_url, ),
            executor.submit(get_ershoufang_house_url, ),
        )
    )

    list(
        as_completed(
            executor.submit(get_ershoufang_house_info, hs)
            for hs, name in HOUSE_DISTRICT_DICT.items()
            if not (RES_DIR / "house_info" / "ershoufang" / f"{hs}.json").is_file()
        )
    )
    list(
        as_completed(
            executor.submit(get_chengjiao_house_info, hs)
            for hs, name in HOUSE_DISTRICT_DICT.items()
            if not (RES_DIR / "house_info" / "chengjiao" / f"{hs}.json").is_file()
        )
    )

    to_csv()


if __name__ == "__main__":
    craw()
