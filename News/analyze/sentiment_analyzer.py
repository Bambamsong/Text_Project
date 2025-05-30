import json
import pandas as pd
import numpy as np
import os

# def score_comments(df: pd.DataFrame, senti_dict_path: str = None) -> pd.DataFrame:
#     """전처리된 DataFrame에 점수 컬럼 추가 후 반환"""
#     # senti_dict_path가 주어지지 않으면, 프로젝트 루트의 data 폴더에서 검색
#     if senti_dict_path is None:
#         # analyze 패키지 디렉토리 기준으로 상위 두 단계(프로젝트 루트) 경로 계산
#         base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#         senti_dict_path = os.path.join(base_dir, 'data', 'SentiWord_info.json')

#     with open(senti_dict_path, encoding='utf-8-sig') as f:
#         senti = pd.DataFrame(json.load(f))
#     senti['polarity'] = pd.to_numeric(senti['polarity'], errors='coerce')

#     def calc(tokens: list) -> float:
#         df_sub = senti[senti['word'].isin(tokens)].dropna(subset=['polarity'])
#         df_sub = df_sub.sort_values(by='polarity', key=lambda x: x.abs()).drop_duplicates('word')
#         return df_sub['polarity'].sum()

#     df = df.copy()
#     df['score'] = df['tokens'].apply(calc)
#     return df

import os
import json
import pandas as pd
import numpy as np

# 감성 사전 경로를 인자로 받으며, 기본값은 None (자동 검색)
def score_comments(df: pd.DataFrame, senti_dict_path: str = None) -> pd.DataFrame:
    """전처리된 DataFrame에 점수 컬럼 추가 후 반환"""
    # 1) 경로가 주어지지 않으면 프로젝트 루트의 data 폴더를 기준으로 탐색
    if senti_dict_path is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        senti_dict_path = os.path.join(base_dir, 'data', 'SentiWord_info.json')
    # 2) 파일 존재 여부 확인
    if not os.path.exists(senti_dict_path):
        raise FileNotFoundError(f"Sentiment dictionary not found at: {senti_dict_path}")
    # 3) JSON 파일 로드
    with open(senti_dict_path, encoding='utf-8-sig') as f:
        senti = pd.DataFrame(json.load(f))
    senti['polarity'] = pd.to_numeric(senti['polarity'], errors='coerce')

    # 4) 토큰 리스트별 점수 계산 함수
    def calc(tokens: list) -> float:
        df_sub = senti[senti['word'].isin(tokens)].dropna(subset=['polarity'])
        df_sub = df_sub.sort_values(by='polarity', key=lambda x: x.abs()).drop_duplicates('word')
        return df_sub['polarity'].sum()

    # 5) 원본 DataFrame 복사 후 score 컬럼 추가
    df_out = df.copy()
    df_out['score'] = df_out['tokens'].apply(calc)
    return df_out