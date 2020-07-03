import re
from typing import List

from lian_jia.config import DATA_DIR
from lian_jia.get_data import HOUSE_DISTRICT
from lian_jia.get_data import dump
from lian_jia.get_data import get


def _get_house_url(type: str) -> List[str]:
    def get_house_url_per_page(district: str, page_id: int) -> List[str]:
        content = get(f"https://cq.lianjia.com/{type}/{district}/pg{page_id}/")
        house_url = map(
            lambda x: x[6:-1],
            re.findall(
                r'href="https://cq\.lianjia\.com/{}/\d+?\.html"'.format(type), content
            ),
        )
        return list(house_url)

    res = []
    for d in HOUSE_DISTRICT:
        for i in range(1, 101):
            res += get_house_url_per_page(d, i)

        dump(list(set(res)), DATA_DIR / "house_url" / type / f"{d}.json")
        res = []


def get_chengjiao_house_url() -> List[str]:
    _get_house_url("chengjiao")


def get_ershoufang_house_url() -> List[str]:
    _get_house_url("ershoufang")
