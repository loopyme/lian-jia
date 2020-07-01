import re
from typing import List

from lian_jia.config import RES_DIR
from lian_jia.request import get
from lian_jia.utils import dump


def _get_house_url(type: str) -> List[str]:
    def get_house_url_per_page(page_id: int) -> List[str]:
        content = get(f'https://cq.lianjia.com/{type}/pg{page_id}/')
        house_url = map(lambda x: x[6:-1],
                        re.findall(r'href="https://cq\.lianjia\.com/{}/\d+?\.html"'.format(type), content))
        return list(house_url)

    res = []
    for i in range(1, 101):
        res += get_house_url_per_page(i)
        dump(res, RES_DIR / "house_url" / type / f"{i}.json")
    dump((res := list(set(res))), RES_DIR / "house_url" / type / "res.json")
    return res


def get_chengjiao_house_url() -> List[str]:
    return _get_house_url("chengjiao")


def get_ershoufang_house_url() -> List[str]:
    return _get_house_url("ershoufang")