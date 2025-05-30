import json
import pandas as pd
import numpy as np

from kiwipiepy import Kiwi
kiwi = Kiwi(typos='basic')

# KNU 한국어 감성어 사전
with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
    sentiword =json.load(f)

df_senti = pd.DataFrame(sentiword)
comment_data = pd.read_csv('../DATA/news_comments.csv')

def preprocess_hangul(my_str, analyzer=kiwi):
    results = kiwi.space(my_str)
    results = kiwi.tokenize(results, 
                            normalize_coda=True, 
                            z_coda=True, 
                            split_complex=False)
    results = [x.form for x in results if x.tag.startswith(('N','V','M','I','W'))]
    return results

df_tmp = comment_data.copy()

df_tmp['preprocessed_comment'] = df_tmp['comment'].apply(lambda x: preprocess_hangul(x))

# def calculate_score(token_list, df_senti = df_senti, standard_col = 'word'):
#     df_score = df_senti[df_senti[standard_col].isin(token_list)]
#     df_score = df_score.sort_values(by='polarity', key = lambda x: np.abs(x))
#     df_score = df_score.drop_duplicates(subset=standard_col, keep='first')
#     score = df_score['polarity'].sum()
#     return score

def calculate_score(token_list, df_senti=df_senti, standard_col='word'):
    df_score = df_senti[df_senti[standard_col].isin(token_list)].copy()
    
    # 🔒 안전하게 float으로 변환
    df_score['polarity'] = pd.to_numeric(df_score['polarity'], errors='coerce')
    
    # # 🔍 NaN 제거 (원한다면)
    df_score = df_score.dropna(subset=['polarity'])

    # 정렬 및 점수 계산
    df_score = df_score.sort_values(by='polarity', key=lambda x: np.abs(x))
    df_score = df_score.drop_duplicates(subset=standard_col, keep='first')
    return df_score['polarity'].sum()
df_tmp['score'] = df_tmp['preprocessed_comment'].apply(lambda x: calculate_score(x))

print(df_tmp['score'].head())
print(df_tmp.groupby('keyword')['score'].value_counts())
# WordCloud
