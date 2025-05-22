# import urllib.parse
# from selenium import webdriver
# import time
import os
# import urllib.request

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("NAVER_ID")
client_secret = os.getenv("NAVER_PW")

# # 네이버 검색 API

# keyword = urllib.parse.quote('김문수')
# url = "https://openapi.naver.com/v1/search/news?query=" + keyword

# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     # print(response_body.decode('utf-8'))
#     print(type(response))
# else:
#     print("Error Code:" + rescode)

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import pandas as pd

def get_news_urls(query, start=1, display=10):
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    url = "https://openapi.naver.com/v1/search/news.json"
    params = {"query": query, "start": start, "display": display, "sort": "sim"}
    res = requests.get(url, headers=headers, params=params)
    items = res.json().get("items", [])
    urls = [item['link'] for item in items]
    return urls

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

# def extract_comments(driver, url):
#     driver.get(url)
#     time.sleep(2)

#     # 댓글 iframe으로 전환
#     try:
#         driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#commentFrame"))
#     except:
#         return []

#     comments = []
#     while True:
#         try:
#             more = driver.find_element(By.CSS_SELECTOR, ".u_cbox_btn_more")
#             more.click()
#             time.sleep(0.5)
#         except:
#             break

#     elements = driver.find_elements(By.CSS_SELECTOR, ".u_cbox_text_wrap .u_cbox_contents")
#     for el in elements:
#         comments.append(el.text.strip())
#     return comments
def extract_comments(driver, url):
    driver.get(url)
    time.sleep(2)

    # 1. 댓글 보기 버튼이 있다면 먼저 클릭
    try:
        comment_button = driver.find_element(By.CSS_SELECTOR, "a.u_cbox_btn_view")  # 댓글 보기 버튼
        comment_button.click()
        time.sleep(2)
    except:
        pass  # 버튼이 없어도 시도는 계속함

    # 2. iframe으로 전환
    try:
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#commentFrame"))
    except:
        print("⚠️ 댓글 iframe 없음")
        return []

    # 3. 더보기 클릭 반복
    comments = []
    while True:
        try:
            more = driver.find_element(By.CSS_SELECTOR, ".u_cbox_btn_more")
            more.click()
            time.sleep(0.5)
        except:
            break

    # 4. 댓글 추출
    elements = driver.find_elements(By.CSS_SELECTOR, ".u_cbox_text_wrap .u_cbox_contents")
    for el in elements:
        comments.append(el.text.strip())

    return comments


def crawl_all_comments(query, total_news=200):
    driver = setup_driver()
    all_comments = []
    
    for start in range(1, total_news+1, 100):
        urls = get_news_urls(query, start=start)
        for url in urls:
            try:
                comments = extract_comments(driver, url)
                if comments:
                    for c in comments:
                        all_comments.append({
                            "query": query,
                            "url": url,
                            "comment": c
                        })
                    print(f"✅ 댓글 수집 완료: {url} ({len(comments)}개)")
                else:
                    print(f"❌ 댓글 없음: {url}")
            except Exception as e:
                print(f"⚠️ 오류 발생: {url} / {e}")
    driver.quit()
    return all_comments

def crawl_10_news_comments(query):
    driver = setup_driver()
    all_comments = []
    
    urls = get_news_urls(query, start=1, display=10)  # 🔸 10개만 가져오기
    for url in urls:
        try:
            comments = extract_comments(driver, url)
            if comments:
                for c in comments:
                    all_comments.append({
                        "query": query,
                        "url": url,
                        "comment": c
                    })
                print(f"✅ 댓글 수집 완료: {url} ({len(comments)}개)")
            else:
                print(f"❌ 댓글 없음: {url}")
        except Exception as e:
            print(f"⚠️ 오류 발생: {url} / {e}")
    driver.quit()
    return all_comments

data = crawl_10_news_comments("이재명")
df = pd.DataFrame(data)
df.to_csv("test_comments_10_news.csv", index=False, encoding='utf-8-sig')