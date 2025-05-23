import pandas as pd
import re

def contains_korean(text):
    return bool(re.search(r'[가-힣]', str(text)))

def clean_comment(text):
    if not isinstance(text, str):
        return ""

    # 1. 이모티콘 제거 (유니코드 이모지 블록)
    text = re.sub(r"[^\w\s\uAC00-\uD7A3]", " ", text)  # 한글, 숫자, 영문, 공백 외 제거

    # 2. 반복되는 ㅋ,ㅎ,ㅜ,ㅠ,ㅡ 등 제거
    text = re.sub(r"[ㅋㅎㅜㅠㅡ]+", " ", text)

    # 3. 줄임말 문자 (ㄱ-ㅎ, ㅏ-ㅣ 등 단독) 제거
    text = re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", " ", text)

    # 4. 반복 특수문자 제거 (예: ... ~~~)
    text = re.sub(r"[.]{2,}", " ", text)
    text = re.sub(r"[~]{2,}", " ", text)

    # 5. 다중 공백 정리
    text = re.sub(r"\s+", " ", text).strip()

    return text

def filter_korean_comments(input_path, output_path):
    df = pd.read_csv(input_path)

    # 한글 포함 댓글만 필터링
    df = df[df['comment'].apply(contains_korean)]

    # 텍스트 정제
    df['comment'] = df['comment'].apply(clean_comment)

    # 공백이나 너무 짧은 댓글 제거
    df = df[df['comment'].str.len() > 1]

    # comment 컬럼만 남기고 저장
    df[['comment']].to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 정제된 한글 댓글만 저장 완료: {output_path}")

if __name__ == "__main__":
    input_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments.csv"
    output_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments_korean_cleaned.csv"
    filter_korean_comments(input_csv, output_csv)
