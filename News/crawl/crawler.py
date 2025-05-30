from selenium import webdriver
from .utils import extract_comments_from_url


def crawl_comments_for(news_dict: dict) -> list:
    """뉴스 딕셔너리에 담긴 각 기사 URL에서 댓글 크롤링"""
    driver = webdriver.Chrome()
    result = []

    for article in news_dict.values():
        url = article['link']
        press = article['platform']
        keyword = article['keyword']
        try:
            comments = extract_comments_from_url(driver, url)
            for c in comments:
                result.append({
                    'platform': 'news',
                    'press': press,
                    'keyword': keyword,
                    'comment': c
                })
        except Exception as e:
            print(f"크롤링 에러: {e}")

    driver.quit()
    return result
