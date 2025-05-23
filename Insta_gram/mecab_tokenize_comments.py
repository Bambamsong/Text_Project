import pandas as pd
import re
from konlpy.tag import Mecab

tagger = Mecab()

def contains_korean(text):
    return bool(re.search(r'[가-힣]', str(text)))

def clean_comment(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^\w\s\uAC00-\uD7A3]", " ", text)  # 이모티콘 및 특수문자 제거
    text = re.sub(r"[ㅋㅎㅜㅠㅡ]+", " ", text)
    text = re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", " ", text)
    text = re.sub(r"[.]{2,}", " ", text)
    text = re.sub(r"[~]{2,}", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_comment(text):
    tokens = tagger.morphs(text)
    return " ".join(tokens)

def process_comments(input_path, output_path):
    df = pd.read_csv(input_path)

    # 1. 한글 포함 댓글 필터
    df = df[df['comment'].apply(contains_korean)]

    # 2. 정제
    df['cleaned'] = df['comment'].apply(clean_comment)

    # 3. 형태소 분석
    df['mecab_tokens'] = df['cleaned'].apply(tokenize_comment)

    # 4. 결과 저장
    df[['comment', 'mecab_tokens']].to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 형태소 분석 결과 저장 완료: {output_path}")

if __name__ == "__main__":
    input_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments.csv"
    output_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments_mecab.csv"
    process_comments(input_csv, output_csv)
