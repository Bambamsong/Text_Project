import pandas as pd
import numpy as np
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords

kiwi = Kiwi(typos='basic')
stopwords = Stopwords()

def preprocess_comments(df: pd.DataFrame) -> pd.DataFrame:
    """댓글 DataFrame에 전처리 컬럼 추가 후 반환"""
    # 본격적인 전처리전 데이터 점검(중복삭제, null 값 제거)
    df = df.drop_duplicates(subset=['comment']).copy()
    df['comment'] = df['comment'].str.strip().replace('', np.nan)
    df = df.dropna(subset=['comment']).reset_index(drop=True)

    def tokenize(text: str) -> list:
        spaced = kiwi.space(text)
        sents = kiwi.split_into_sents(spaced)
        tokens = []
        for sent in sents:
            for token in kiwi.tokenize(sent.text):
                if token.tag.startswith(('NNG','NNP','VV','VA')) and (token.form, token.tag) not in stopwords:
                    tokens.append(token.form)
        return tokens

    df['tokens'] = df['comment'].apply(tokenize)
    return df