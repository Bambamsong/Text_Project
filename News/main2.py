import os
import urllib.parse
from dotenv import load_dotenv
import urllib
import json
import html
import re
from fucntion import platform_list
# env파일 사용
load_dotenv()

client_id = os.getenv('NAVER_ID')
client_secret = os.getenv('NAVER_PW')

base_url = 'https://openapi.naver.com/v1/search/news.json'
query = '이재명'
encQuery = urllib.parse.quote(query) # 한글이나 특수문자가 포함된 검색어(쿼리)를 URL에 안전하게 쓸 수 있도록 인코딩해주는 것
n_display = 100
start = 1
sort = 'sim'

# 최종 URL 구조
url = f'{base_url}?query={encQuery}&display={n_display}&start={start}&sort={sort}'

# 네이버 검색 API 호출
## HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿을 추가해야함

import requests

headers = {
    'X-Naver-Client-Id': client_id,
    'X-Naver-Client-Secret': client_secret
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data['items'], indent=2, ensure_ascii=False))
else:
    print('❌ 요청 실패 ', response.status_code)

data = data['items']
data1 = data.copy()

all_result = dict()
i = 0
for news in data1:
    link = html.unescape(news['link'])
    pubdate = news['pubDate']

    if 'n.news.naver.com' in link:
        all_result[i] = dict()
        all_result[i]['link'] = link
        match = re.search(r'article/(\d+)', link)
        if match:
            press_code = match.group(1)
            press_name = platform_list.get(press_code, '기타')
        else:
            press_name = '기타'
        all_result[i]['platform'] = press_name
        all_result[i]['pubdate'] = pubdate
        i += 1

all_result