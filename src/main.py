"""
每日热点新闻集锦 - 主程序
"""
import json
import os
import sys
from datetime import datetime
from sources.weibo import get_weibo_hot
from sources.baidu import get_baidu_hot
from sources.zhihu import get_zhihu_hot
from sources.bilibili import get_bilibili_hot

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

SOURCES = [
    ("微博热搜", get_weibo_hot),
    ("百度热搜", get_baidu_hot),
    ("知乎热榜", get_zhihu_hot),
    ("B站热门", get_bilibili_hot),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# 每日热点新闻集锦 - {today}\n"]

    for name, fetcher in SOURCES:
        print(f"[*] 正在抓取 {name}...")
        try:
            items = fetcher()
            lines.append(f"\n## {name}\n")
            for i, item in enumerate(items[:20], 1):
                title = item.get("title", "")
                url = item.get("url", "")
                hot = item.get("hot", "")
                hot_str = f" [{hot}]" if hot else ""
                if url:
                    lines.append(f"{i}. [{title}]({url}){hot_str}")
                else:
                    lines.append(f"{i}. {title}{hot_str}")
        except Exception as e:
            lines.append(f"\n## {name}\n")
            lines.append(f"抓取失败: {e}\n")

    content = "\n".join(lines)
    output_file = os.path.join(OUTPUT_DIR, f"hot-news-{today}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n[OK] 已保存到: {output_file}")


if __name__ == "__main__":
    main()
