import json
import re

from lian_jia.config import HOUSE_VALUES, RES_DIR
from lian_jia.request import get
from lian_jia.utils import dump


def _get_basic_house_info_per_house(web_content: str):
    res = {}
    for p in HOUSE_VALUES:
        re_res = re.search(
            r'<li><span class="label">{}</span>.+?</li>'.format(p), web_content
        )
        if re_res is None:
            continue
        res[p] = re_res.group(0).split("</span>")[-1][:-5].strip(" ")
    return res


def get_chengjiao_house_info_per_house(house_url: str):
    content = get(house_url)
    res = _get_basic_house_info_per_house(content)

    # 价格
    re_res = re.search(
        r'<div class="price"><span class="dealTotalPrice"><i>(\d|.)+?</i>万</span>'
        r"<b>(\d|.)+?</b>元/平",
        content,
    )
    if re_res is not None:
        res["成交单价(元/平)"] = re_res.group(0).split("<b>")[-1][:-7]
        res["成交总价(万元)"] = re_res.group(0).split("</i>")[0][51:]

    re_res = re.search(r"<label>(\d|.)+?</label>挂牌价格（万）", content)
    if re_res is not None:
        res["挂牌总价(万元)"] = re_res.group(0).rstrip("</label>挂牌价格（万）")[7:]

    # 成交周期
    re_res = re.search(r"</span><span><label>\d+?</label>成交周期（天）</span>", content)
    if re_res is not None:
        res["成交周期(天)"] = re_res.group(0).split("</label>")[0][20:]
    return res


def get_ershoufang_house_info_per_house(house_url: str):
    content = get(house_url)
    res = _get_basic_house_info_per_house(content)

    # price
    re_res = re.search(
        r'</div><div class="price "><span class="total">(\d|.)+?</span><span class="unit"><span>万</span></span>'
        r'<div class="text"><div class="unitPrice"><span class="unitPriceValue">(\d|.)+?<i>元/平米</i>',
        content,
    )
    if re_res is not None:
        res["挂牌单价(元/平)"] = re_res.group(0).split('<span class="unitPriceValue">')[-1][
                           :-11
                           ]
        res["挂牌总价(万元)"] = re_res.group(0).split("</span>")[0][46:]

    return res


def get_ershoufang_house_info(house_district: str):
    res = []
    with open(
            RES_DIR / "house_url" / "ershoufang" / f"{house_district}.json", "r"
    ) as f:
        url_list = json.loads(f.read())
    print(f"Load success, find {len(url_list)} urls. Start to get house info from it.")
    for i, url in enumerate(url_list):
        if i % 100 == 0:
            print(house_district, i, len(url_list))
        res.append(get_ershoufang_house_info_per_house(url))

    dump(res, RES_DIR / "house_info" / "ershoufang" / f"{house_district}.json")


def get_chengjiao_house_info(house_district: str):
    res = []
    with open(RES_DIR / "house_url" / "chengjiao" / f"{house_district}.json", "r") as f:
        url_list = json.loads(f.read())
    print(f"Load success, find {len(url_list)} urls. Start to get house info from it.")
    for i, url in enumerate(url_list):
        if i % 100 == 0:
            print(house_district, i, len(url_list))
        res.append(get_chengjiao_house_info_per_house(url))

    dump(res, RES_DIR / "house_info" / "chengjiao" / f"{house_district}.json")
