# kiwi_module/saver.py

from Insta_gram.anlayze.kiwi_module import KiwiNounExtractor

def extract_and_save_nouns_from_csv(csv_path: str, output_path: str, text_column: str = "comment") -> None:
    """
    KiwiNounExtractor를 사용하여 명사 추출 후 CSV로 저장
    """
    extractor = KiwiNounExtractor()
    df = extractor.extract_nouns_from_csv(csv_path, text_column)
    df.to_csv(output_path, index=False)
    print(f"✅ 저장 완료: {output_path}")

# 테스트 실행용
if __name__ == "__main__":
    input_path = "/home/kang/PythonProject/Project 1./Text_Project/DATA/instagram_comments_korean_cleaned.csv"
    output_path = "/home/kang/PythonProject/Project 1./Text_Project/DATA/with_nouns.csv"

    extract_and_save_nouns_from_csv(input_path, output_path)
