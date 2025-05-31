# cloud.py

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordCloudGenerator:
    def __init__(self, csv_path: str):
        """
        명사 컬럼이 포함된 CSV 파일을 로드합니다.
        """
        self.df = pd.read_csv(csv_path)
        if 'keyword' not in self.df.columns or 'nouns' not in self.df.columns:
            raise ValueError("CSV 파일에는 'keyword'와 'nouns' 컬럼이 포함되어야 합니다.")
        
        # 문자열 형태의 리스트라면 리스트로 복원
        if isinstance(self.df['nouns'].iloc[0], str):
            self.df['nouns'] = self.df['nouns'].apply(eval)

    def get_noun_text_by_keyword(self, keyword: str) -> str:
      """
      주어진 키워드에 해당하는 명사 리스트를 하나의 문자열로 반환
      - 한 글자인 단어 제거
      - 키워드와 동일한 단어 제거
      """
      filtered = self.df[self.df['keyword'] == keyword]
      if filtered.empty:
          raise ValueError(f"❌ 키워드 '{keyword}'에 해당하는 데이터가 없습니다.")
      
      all_nouns = [noun for nouns in filtered['nouns'] for noun in nouns]

      # 전처리: 한 글자 제외 + 키워드 단어 제거
      cleaned_nouns = [noun for noun in all_nouns if len(noun) > 1 and noun != keyword]

      if not cleaned_nouns:
          raise ValueError(f"❌ 키워드 '{keyword}'에 대한 유효한 명사가 없습니다.")
      
      return ' '.join(cleaned_nouns)

    def show_wordcloud(self, keyword: str, max_words: int = 100):
        """
        화면에 워드클라우드를 표시합니다.
        """
        text = self.get_noun_text_by_keyword(keyword)
        wc = WordCloud(
            font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # 시스템에 맞게 조정
            width=800,
            height=400,
            background_color="white",
            max_words=max_words
        ).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def save_wordcloud(self, keyword: str, save_path: str, max_words: int = 100):
        """
        워드클라우드를 이미지 파일로 저장합니다.
        """
        text = self.get_noun_text_by_keyword(keyword)
        wc = WordCloud(
            font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # 한글 폰트 경로
            width=800,
            height=400,
            background_color="white",
            max_words=max_words
        ).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"✅ 워드클라우드 저장 완료: {save_path}")
