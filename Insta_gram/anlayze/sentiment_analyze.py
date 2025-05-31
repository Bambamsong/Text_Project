import pandas as pd
import json

class KoreanSentimentAnalyzer:
    def __init__(self, csv_path: str, sentiword_json_path: str):
        # 댓글 데이터 로드
        self.df = pd.read_csv(csv_path)
        self.df['nouns_adjs'] = self.df['nouns_adjs'].apply(eval)

        # 감성사전 로드 (JSON)
        with open(sentiword_json_path, 'r', encoding='utf-8') as f:
            senti_data = json.load(f)

        # 단어별 감성 점수 딕셔너리로 변환
        self.senti_dict = {entry['word']: float(entry['polarity']) for entry in senti_data if 'word' in entry and 'polarity' in entry}

    def compute_sentiment_score(self, word_list: list) -> float:
        """
        단어 리스트에 대해 감성 점수 합산
        """
        score = 0
        for word in word_list:
            if word in self.senti_dict:
                score += self.senti_dict[word]
        return score

    def analyze_keyword_sentiment(self, keyword: str) -> float:
        """
        주어진 keyword에 해당하는 댓글들의 평균 감성 점수를 반환
        """
        filtered_df = self.df[self.df['keyword'] == keyword]
        if filtered_df.empty:
            raise ValueError(f"❌ 키워드 '{keyword}'에 해당하는 데이터가 없습니다.")

        filtered_df['sentiment_score'] = filtered_df['nouns_adjs'].apply(self.compute_sentiment_score)
        return filtered_df['sentiment_score'].mean()
