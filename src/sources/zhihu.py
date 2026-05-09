"""
知乎热榜抓取 - 使用头条热榜代替(因为知乎API严格防爬)
"""
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get_zhihu_hot() -> list[dict]:
    """返回今日头条热榜(作为知乎替代)"""
    items = []

    # 今日头条热榜(不需要cookie)
    try:
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("data", []):
                title = item.get("Title", "") or item.get("title", "")
                url_str = item.get("Url", "") or item.get("url", "")
                hot = item.get("HotValue", "") or item.get("hot_value", "")
                if title:
                    items.append({
                        "title": title,
                        "url": url_str,
                        "hot": str(hot),
                    })
    except:
        pass

    if items:
        return items

    # 完全备用: 直接用百度热搜(防知乎挂掉)
    try:
        from sources.baidu import get_baidu_hot
        items = get_baidu_hot()[:10]
    except:
        pass

    return items
