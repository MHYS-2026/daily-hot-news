#!/usr/bin/env python
"""
每日热点新闻 → 公众号文章 + 封面图 一键生成
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SRC_DIR = os.path.join(BASE_DIR, "src")

def step(msg):
    print(f"\n{'='*50}")
    print(f"[*] {msg}")
    print(f"{'='*50}")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] 错误: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

def main():
    step("1/3 抓取今日热点新闻")
    run_cmd(f"cd {BASE_DIR} && python src/main.py")
    
    step("2/3 生成公众号封面图")
    run_cmd(f"cd {OUTPUT_DIR} && python gen_cover.py")
    
    step("3/4 生成公众号排版Word文档")
    run_cmd(f"cd {OUTPUT_DIR} && python gen_wechat_docx.py")
    
    step("4/4 一键推送至 GitHub")
    run_cmd(f"cd {BASE_DIR} && git add . && git commit -m \"📰 每日热点 {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\" --quiet && git push")
    
    today = __import__('datetime').datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"\n{'='*50}")
    print("[OK] 全部完成！")
    print(f"[文章]: {OUTPUT_DIR}\\wechat-article-{date_str}.md")
    print(f"[Word]: {OUTPUT_DIR}\\wechat-article-{date_str}.docx")
    print(f"[封面]: {OUTPUT_DIR}\\cover-{date_str}.jpg")
    print(f"\n[三步发公众号]:")
    print(f"   1. 打开 Word -> 全选复制")
    print(f"   2. 粘贴到公众号后台")
    print(f"   3. 上传封面图 -> 发布")

if __name__ == "__main__":
    main()
