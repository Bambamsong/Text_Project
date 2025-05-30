import re
import requests
import json
import html

import time
from selenium.webdriver.common.by import By
from selenium import webdriver
platform_list = {
    "001": "연합뉴스",
    "005": "국민일보",
    "011": "서울경제",
    "014": "파이낸셜뉴스",
    "015": "한국경제",
    "016": "헤럴드경제",
    "018": "한겨레",
    "020": "동아일보",
    "021": "문화일보",
    "022": "세계일보",
    "023": "조선일보",
    "025": "중앙일보",
    "028": "한겨레",
    "032": "경향신문",
    "033": "주간경향",
    "038": "한국일보",
    "055": "SBS",
    "056": "KBS",
    "057": "MBC",
    "081": "서울신문",
    "082": "부산일보",
    "087": "강원일보",
    "088": "경남신문",
    "089": "경북일보",
    "090": "대전일보",
    "091": "매일신문",
    "092": "영남일보",
    "093": "울산신문",
    "094": "전남일보",
    "095": "전북일보",
    "096": "제주일보",
    "097": "중도일보",
    "098": "충북일보",
    "099": "충청일보",
    "100": "강원도민일보",
    "101": "경기일보",
    "102": "경남도민일보",
    "103": "경북도민일보",
    "104": "광주일보",
    "105": "대구일보",
    "106": "대전투데이",
    "107": "동양일보",
    "108": "무등일보",
    "109": "부산일보",
    "110": "서울일보",
    "111": "세계타임즈",
    "112": "울산매일",
    "113": "인천일보",
    "114": "전라일보",
    "115": "전북도민일보",
    "116": "제주신보",
    "117": "중부매일",
    "118": "충북도민일보",
    "119": "충청타임즈",
    "120": "한라일보",
    "121": "헤럴드경제"
}
# 태그를 지우는 함수
def remove_tag(my_str):
    p = re.compile('(<([^>]+)>)')
    return p.sub('', my_str)


# 네이버 API 요청 코드
def get_naver_news(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print(json.dumps(data['items'], indent=2,  ensure_ascii=False)) # 터미널로그상 json 구조를 명확히 보기 위한 코드
    else:
        print('API 요청 실패', response.status_code)
    
    data = data['items']

    return data


# DATA 재구성 함수 (링크, 방송사, 게재일시, 검색 키워드)
def rebase_data(data, query):
    rebase_data = dict()
    i = 0

    for news in data:
        link = html.unescape(news['link'])
        pubdate = news['pubDate']

        if 'n.news.naver.com' in link:
            rebase_data[i] = dict()
            rebase_data[i]['link'] = link
            match = re.search(r'article/(\d+)', link)
            if match:
                press_code = match.group(1)
                press_name = platform_list.get(press_code, '기타')
            else:
                press_name = '기타'
            rebase_data[i]['platform'] = press_name
            rebase_data[i]['pubdate'] = pubdate
            rebase_data[i]['keyword'] = query

        i += 1
    
    return rebase_data


# URL 로부터 댓글을 수집하는 함수
def extract_comments_from_url(driver, url):
    print(f"기사 접속 : {url}")
    driver.get(url)
    time.sleep(1)

    # # 1. 댓글 보기 버튼 클릭
    # 댓글 보기 버튼 클래스 후보 리스트
    possible_classes = [
        'simplecmt_link_text',
        'u_cbox_in_view_comment',
        'u_cbox_ico_view_comment'

    ]

    # 1. 댓글 보기 버튼 찾기
    comment_button_found = False
    for cls in possible_classes:
        try:
            comment_btn = driver.find_element(By.CLASS_NAME, cls)
            comment_btn.click()
            comment_button_found = True
            time.sleep(1.5)
            break  # 성공했으니 루프 종료
        except:
            continue  # 다음 클래스명 시도
    
    if not comment_button_found:
        print("❌ 댓글 보기 버튼 없음\n")
        return []
    
    # 2. 댓글 보기 버튼을 누른 뒤 더보기 버튼 반복하기
    while True:
        try:
            more_btn = driver.find_element(By.CLASS_NAME, 'u_cbox_page_more')
            more_btn.click()
            time.sleep(1)
        except:
            break
    
    # 3. 모든 댓글 수집하기
    comments = []
    try:
        comment_element = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
        for comment in comment_element:
            comments.append(comment.text.strip())
    except:
        print("⚠️ 댓글 수집 중 오류 발생")

    return comments


# 크롤링 함수(링크로부터 댓글 수집)
def crawl_comments(news_dict):
    driver = webdriver.Chrome()

    result = []

    for article in news_dict.values():
        url = html.unescape(article['link'])
        platform = article['platform']
        keyword = article['keyword']

        print(f"[{platform}] : 기사 접속 중 ")
        i = 0
        try:
            comments = extract_comments_from_url(driver, url)
            if comments:
                for c in comments:
                    result.append(
                        {
                            'platform' : 'news',
                            'press' : platform,
                            'keyword' : keyword,
                            'comment' : c
                        }
                    )
                    i += 1
                print(f"댓글 {i}개 수집 완료")
            else:
                print("댓글 없음")
        except:
            print("크롤링 에러")
    driver.quit()

    print(f"총 : {len(result)}개 수집")
    return result











