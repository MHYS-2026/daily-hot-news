"""
B站热门视频抓取
"""
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_bilibili_hot() -> list[dict]:
    """抓取B站热门视频"""
    url = "https://api.bilibili.com/x/web-interface/popular"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    data = resp.json()
    items = []
    for v in data.get("data", {}).get("list", []):
        items.append({
            "title": v.get("title", ""),
            "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
            "hot": f"播放:{v.get('stat', {}).get('view', '')}",
        })
    return items
