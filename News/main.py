import os
from dotenv import load_dotenv
import urllib.parse
import pandas as pd

from fucntion import get_naver_news, rebase_data, extract_comments_from_url, crawl_comments
load_dotenv()

# API 이용 KEY
client_id = os.getenv('NAVER_ID')
client_secret = os.getenv('NAVER_PW')

# API 형식
base_url = 'https://openapi.naver.com/v1/search/news.json'
query = ['이재명', '김문수', '이준석']
n_display = 50
start = 1
sort = 'sim'

headers = {
    'X-Naver-Client-Id': client_id,
    'X-Naver-Client-Secret': client_secret
}


df_all = pd.DataFrame()

for i in query:
    encQuery = urllib.parse.quote(i) # 한글이나 특수문자가 포함된 검색어(쿼리)를 URL에 안전하게 쓸 수 있도록 인코딩해주는 것
    url = url = f'{base_url}?query={encQuery}&display={n_display}&start={start}&sort={sort}'
    
    news_data = get_naver_news(url, headers)

    rebase_news_data = rebase_data(news_data, i)

    result = crawl_comments(rebase_news_data)
    df_result = pd.DataFrame(result)

    df_all = pd.concat([df_all,df_result], ignore_index=True)

    
df_all.to_csv('news_comments.csv', index=False)