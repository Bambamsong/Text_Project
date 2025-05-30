from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
import pandas as pd
import os
import numpy as np
import copy
import re

import time
# print(os.path.exists('../DATA/news_comments.csv')) 

# wordcloud에서 한글을 사용할 수 있도록 설정하기
font_path = '~/Library/Fonts/NanumGothic-Regular.ttf'

data = pd.read_csv('../DATA/'+'news_comments.csv')

kiwi = Kiwi()
# 1. 데이터 체크
def check_data(data):

    print('전처리 전 학습용 샘플의 개수 : ',len(data))
    data.drop_duplicates(subset = ['comment'], inplace = True) # comment 열에서 중복 내용이 있다면 중복 제거
    data['comment'] = data['comment'].str.replace('^ +', "")
    data['comment'] = data['comment'].replace('', np.nan) # document column이 비어있다면(공백), Null 값으로 변경
    data = data.dropna(how='any')
    data = data.reset_index(drop=True) # index reset
    print('전처리 후 학습용 샘플의 개수 :',len(data))

# 2. Kiwi 형태소 분석기를 사용하여 전처리
kiwi = Kiwi(typos='basic')
stopwords = Stopwords()
# def preprocess_korean(text, analyzer=kiwi, stowords=stopwords):
#     my_text = copy.copy(text)
#     my_text = my_text.replace('\n', ' ') # (1) 줄바꿈 문자 제거
#     my_text = kiwi.space(my_text) # (2) 띄어쓰기 교정
#     sents = kiwi.split_into_sents(my_text) # (3) 문장 토큰화
#     p = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]')
#     all_result = []
#     for sent in sents:
#         token_result = kiwi.tokenize(sent.text, stopwords=stopwords) # (4) 형태소 분석 + 간단한 오타 교정
#         token_result = kiwi.join(token_result)
#         token_result = p.sub('', token_result) # (5) 특수 문자 제거 (=한글을 제외한 문자 제거)
#         all_result.append(token_result) # (6) 형태소 분석한 결과를 다시 join
    
#     all_result = ' '.join(all_result) # (7) 모든 문장을 하나의 string으로 join

#     return all_result
def preprocess_korean(text, analyzer=kiwi, stopwords=stopwords):
    my_text = copy.copy(text)
    my_text = my_text.replace('\n', ' ')
    my_text = analyzer.space(my_text)
    sents = analyzer.split_into_sents(my_text)

    noun_result = []
    for sent in sents:
        tokens = analyzer.tokenize(sent.text)
        for token in tokens:
            if token.tag.startswith('NNG') or token.tag.startswith('NNP') or token.tag.startswith('VV') or token.tag.startswith('VA'):
                if (token.form, token.tag) not in stopwords:  # 수정된 부분
                    noun_result.append(token.form)

    return ' '.join(noun_result)

# start = time.time()
# data['preprocessed_comments'] = data['comment'].apply(lambda x: preprocess_korean(x))

# # 1. 저장 경로 구성 (상대 경로)
# save_path = os.path.join(os.path.dirname(__file__), '..', 'DATA', 'preprocessed_news_comments.csv')

# # 2. 상위 폴더가 존재하지 않으면 생성 (안전장치)
# os.makedirs(os.path.dirname(save_path), exist_ok=True)

# # 3. CSV로 저장
# data.to_csv(save_path, index=False, encoding='utf-8-sig')
# end = time.time()
# print(f"Wall time: {end - start:.2f} seconds")

data2 = pd.read_csv('../DATA/'+'preprocessed_news_comments.csv')

def combine_text(data):
    result = {}
    candidates = data['keyword'].dropna().unique()

    for candidate in candidates:
        subset = data[data['keyword'] == candidate] 
        comments = subset['preprocessed_comments'].dropna().astype(str).tolist()
        joined = ' '.join(comments)
        result[candidate] = joined        
    return result

han_news = data2[data2['press']=='연합뉴스']
text = combine_text(han_news)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordclouds(comment_dict, font_path=font_path, figsize=(10, 10)):
    """
    후보자별 댓글 워드클라우드를 생성하고 출력하는 함수

    Parameters:
    - comment_dict: dict, {후보자명: '댓글 문자열'}
    - font_path: str, 워드클라우드에 사용할 한글 폰트 경로
    - figsize: tuple, 출력 이미지 크기
    - title_suffix: str, 제목 뒤에 붙일 문자열
    """
    
    for candidate, text in comment_dict.items():
        wordcloud = WordCloud(
            font_path=font_path,
            background_color='white'
        ).generate(text)

        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        filename = f"{candidate}_wordcloud.png"
        plt.savefig(filename, bbox_inches='tight')

        # 파일 이름 만들기 (후보자명에 특수문자 제거 또는 변환 권장)
        plt.close()  # 화면에 표시하지 않고 바로 저장만

        print(f"✅ 저장됨: {filename}")

generate_wordclouds(text)
