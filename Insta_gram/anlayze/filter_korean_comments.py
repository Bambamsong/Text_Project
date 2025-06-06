import pandas as pd
import re

def contains_korean(text):
    return bool(re.search(r'[가-힣]', str(text)))

def clean_comment(text):
    if not isinstance(text, str):
        return ""

    # 1. 이모티콘 및 특수문자 제거
    text = re.sub(r"[^\w\s\uAC00-\uD7A3]", " ", text)

    # 2. 반복되는 ㅋ,ㅎ,ㅜ,ㅠ,ㅡ 등 제거
    text = re.sub(r"[ㅋㅎㅜㅠㅡ]+", " ", text)

    # 3. 줄임문자 제거 (ㄱ-ㅎ, ㅏ-ㅣ 등 단독 자모)
    text = re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", " ", text)

    # 4. 반복 특수문자 제거
    text = re.sub(r"[.]{2,}", " ", text)
    text = re.sub(r"[~]{2,}", " ", text)

    # 5. 다중 공백 정리
    text = re.sub(r"\s+", " ", text).strip()

    return text

def filter_korean_comments(input_path, output_path):
    df = pd.read_csv(input_path)

    # 한글 포함 댓글만 필터링
    df = df[df['comment'].apply(contains_korean)]

    # 댓글 정제
    df['comment'] = df['comment'].apply(clean_comment)

    # 너무 짧은 댓글 제거
    df = df[df['comment'].str.len() > 1]

    # 'keyword'와 'comment'만 저장
    if 'keyword' in df.columns:
        df[['keyword', 'comment']].to_csv(output_path, index=False, encoding='utf-8-sig')
    else:
        print("⚠️ 'keyword' 컬럼이 존재하지 않아 comment만 저장합니다.")
        df[['comment']].to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"✅ 정제된 댓글 저장 완료: {output_path}")

if __name__ == "__main__":
    input_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments.csv"
    output_csv = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments_korean_cleaned.csv"
    filter_korean_comments(input_csv, output_csv)
