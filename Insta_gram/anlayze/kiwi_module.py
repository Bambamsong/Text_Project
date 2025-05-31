import pandas as pd
from kiwipiepy import Kiwi

class KiwiNounExtractor:
    def __init__(self):
        self.kiwi = Kiwi()

    def extract_nouns_from_text(self, text: str) -> list:
        """
        문장에서 명사만 추출
        """
        tokens = self.kiwi.tokenize(text)
        return [token.form for token in tokens if token.tag.startswith("NN")]

    def extract_nouns_from_csv(self, csv_path: str, text_column: str = "comment") -> pd.DataFrame:
        """
        CSV에서 주어진 열의 텍스트를 명사로 변환하여 DataFrame 반환
        """
        df = pd.read_csv(csv_path)
        df['nouns'] = df[text_column].astype(str).apply(self.extract_nouns_from_text)
        return df[['keyword', text_column, 'nouns']]

def save_df_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    추출된 명사 포함 DataFrame을 CSV로 저장
    """
    df.to_csv(output_path, index=False)
    print(f"✅ 저장 완료: {output_path}")