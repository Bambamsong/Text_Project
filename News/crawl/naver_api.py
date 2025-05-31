import requests
import html
import re
from .utils import platform_list

def fetch_news_items(query: str, base_url: str, headers: dict, n_display: int = 30, start: int = 1, sort: str = 'sim') -> dict:
    """네이버 API 호출 후 rebase_data를 통해 딕셔너리 형태로 반환"""
    enc_query = requests.utils.requote_uri(query)
    url = f"{base_url}?query={enc_query}&display={n_display}&start={start}&sort={sort}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json().get('items', [])
    return rebase_data(items, query)


def rebase_data(data: list, query: str) -> dict:
    """API 반환 items를 재구성하여 link, platform, pubdate, keyword 포함"""
    rebase = {}
    for i, news in enumerate(data):
        link = html.unescape(news.get('link', ''))
        if 'n.news.naver.com' not in link:
            continue
        match = re.search(r'article/(\d+)', link)
        press_code = match.group(1) if match else None
        press_name = platform_list.get(press_code, '기타')
        rebase[i] = {
            'link': link,
            'platform': press_name,
            'pubdate': news.get('pubDate', ''),
            'keyword': query
        }
    return rebase