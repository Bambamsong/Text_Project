import re
from selenium.webdriver.common.by import By
import time

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
    "091": "매일신문"
}

# 태그를 지우는 함수
def remove_tag(my_str):
    p = re.compile('(<([^>]+)>)')
    return p.sub('', my_str)

# 셀레니움을 이용해 네이버 뉴스 댓글 추출
def extract_comments_from_url(driver, url: str) -> list:
    """셀레니움을 이용해 네이버 뉴스 댓글 추출"""
    driver.get(url)
    time.sleep(1)
    # 댓글 보기 버튼 리스트
    classes = ['simplecmt_link_text', 'u_cbox_in_view_comment', 'u_cbox_ico_view_comment']
    for cls in classes:
        try:
            btn = driver.find_element(By.CLASS_NAME, cls)
            btn.click()
            time.sleep(1)
            break
        except:
            continue
    # 더보기 클릭
    while True:
        try:
            more = driver.find_element(By.CLASS_NAME, 'u_cbox_page_more')
            more.click()
            time.sleep(0.5)
        except:
            break
    # 댓글 수집
    comments = []
    elems = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    for el in elems:
        comments.append(el.text.strip())
    return comments