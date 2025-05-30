import os
import pandas as pd
from dotenv import load_dotenv

from crawl import fetch_news_items, crawl_comments_for
from preprocess import preprocess_comments, generate_wordclouds
from analyze import score_comments

dict_path = 'data/SentiWord_info.json'
def main():
    load_dotenv()
    client_id = os.getenv('NAVER_ID')
    client_secret = os.getenv('NAVER_PW')
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    base_url = 'https://openapi.naver.com/v1/search/news.json'
    queries = ['이재명', '김문수', '이준석']
    all_comments = []

    for q in queries:
        news_dict = fetch_news_items(q, base_url, headers)
        comments = crawl_comments_for(news_dict)
        all_comments.extend(comments)

    df_comments = pd.DataFrame(all_comments)
    df_comments.to_csv('output/raw_data/raw_news_comments.csv', index = False, encoding='utf-8-sig') # 파일 별도 저장

    df_pre = preprocess_comments(df_comments)
    senti_dict_path = os.path.join(os.getcwd(), 'data', 'SentiWord_info.json')
    df_scored = score_comments(df_pre, senti_dict_path=senti_dict_path)

    generate_wordclouds(df_pre, font_path='~/Library/Fonts/NanumGothic-Regular.ttf', out_dir='output/wordclouds')

    os.makedirs('data', exist_ok=True)
    df_scored.to_csv('output/comments_score/news_comments_scored.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()