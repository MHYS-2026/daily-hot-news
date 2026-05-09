"""
百度热搜抓取
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_baidu_hot() -> list[dict]:
    """抓取百度热搜"""
    url = "https://top.baidu.com/board?tab=realtime"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "lxml")
    items = []
    for card in soup.select(".category-wrap_iQLoo"):
        title_el = card.select_one(".c-single-text-ellipsis")
        link_el = card.select_one("a")
        hot_el = card.select_one(".hot-index_1Bl1a")
        title = title_el.text.strip() if title_el else ""
        href = link_el.get("href", "") if link_el else ""
        hot = hot_el.text.strip() if hot_el else ""
        items.append({"title": title, "url": href, "hot": hot})
    return items
