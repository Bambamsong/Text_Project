import os
from wordcloud import WordCloud


def generate_wordclouds(df, font_path: str, out_dir: str):
    """토큰 컬럼을 이용해 후보자별 워드클라우드 저장"""
    os.makedirs(out_dir, exist_ok=True)
    grouped = df.groupby('keyword')['tokens']
    for keyword, series in grouped:
        text = ' '.join([' '.join(tokens) for tokens in series])
        wc = WordCloud(font_path=font_path, background_color='white').generate(text)
        path = os.path.join(out_dir, f"{keyword}_wordcloud.png")
        wc.to_file(path)
        print(f"✅ 저장됨: {path}")