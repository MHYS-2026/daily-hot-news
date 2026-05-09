"""
微博热搜抓取 - 通过第三方聚合接口获取
"""
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://weibo.com/",
}


def get_weibo_hot() -> list[dict]:
    """从微博热搜榜获取"""
    items = []

    # API方式(可能需要cookie)
    url = "https://weibo.com/ajax/side/hotSearch"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("data", {}).get("realtime", []):
                word = item.get("word", "")
                if word:
                    items.append({
                        "title": word,
                        "url": f"https://s.weibo.com/weibo?q={word}",
                        "hot": f"热度:{item.get('raw_hot', '')}",
                    })
    except:
        pass

    # 如果API失败，用Tencen新闻聚合接口(免认证)
    if not items:
        try:
            resp = requests.get(
                "https://news.qq.com/omn/20200522/20200522A0Q1X100.html",
                headers=HEADERS, timeout=10)
        except:
            pass
        if not items:
            # 最稳定的备用: 使用新浪热点迷你版
            try:
                resp = requests.get(
                    "https://weibo.com/ajax/statuses/hot_band",
                    headers={**HEADERS, "X-Requested-With": "XMLHttpRequest"},
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("data", {}).get("band_list", []):
                        word = item.get("word", "")
                        note = item.get("note", "")
                        title = note or word
                        if title:
                            items.append({
                                "title": title,
                                "url": f"https://s.weibo.com/weibo?q={word}",
                                "hot": f"热度:{item.get('raw_hot', '')}",
                            })
            except:
                pass

    return items
