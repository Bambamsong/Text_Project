# News Comments Sentiment & Wordcloud Pipeline

파이썬으로 네이버 뉴스 댓글을 크롤링하고 전처리하여 감성 분석 및 워드클라우드를 생성하는 모듈화된 프로젝트입니다.

## 폴더 구조

~~~
project-root/
│
├─ crawl/
│ ├─ __init__.py # 패키지 초기화 및 함수 import
│ ├─ naver_api.py # 네이버 뉴스 API 호출 및 데이터 재구성
│ ├─ utils.py # 댓글 추출, HTML 태그 제거 등 유틸 함수
│ └─ crawler.py # 셀레니움을 이용한 댓글 크롤러 진입점
│
├─ preprocess/
│ ├─ __init__.py # 패키지 초기화 및 함수 import
│ ├─ text_preprocessor.py # 댓글 텍스트 정제 및 토크나이징
│ └─ wordcloud_generator.py# 토큰 기반 워드클라우드 생성
│
├─ analyze/
│ ├─ __init__.py # 패키지 초기화 및 함수 import
│ └─ sentiment_analyzer.py # 감성 사전 기반 점수 계산
│
├─ data/ # CSV, JSON 등 원시 및 중간 데이터 저장
├─ output/ # 워드클라우드, 시각화 결과 저장
│
├─ main.py # 전체 파이프라인 실행 진입점
├─ requirements.txt # 프로젝트 의존 라이브러리 목록
└─ .gitignore # Git 무시 파일 설정
~~~


## 주요 기능

1. **크롤링** (`crawl` 패키지)  
   - 네이버 뉴스 API를 통해 기사 링크 수집  
   - 셀레니움을 이용해 각 기사 댓글 크롤링  

2. **전처리** (`preprocess` 패키지)  
   - 중복 및 결측치 제거  
   - 형태소 분석(Kiwi)을 통한 토큰화  
   - 토큰 리스트로 저장 및 워드클라우드 이미지 생성  

3. **감성 분석** (`analyze` 패키지)  
   - KNU 감성 사전 기반 단어별 polarity 합산  
   - 댓글별 점수 계산 및 DataFrame에 추가  

4. **결과 저장**  
   - 중간 결과: `data/raw_news_comments.csv`  
   - 최종 결과: `data/news_comments_scored.csv`  
   - 워드클라우드: `output/wordclouds/{keyword}_wordcloud.png`  

## 설치 및 실행

1. **의존성 설치**  
프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 추가하세요.
(프로젝트와 무관한 패키지들이 존재하여 가상환경을 만드시길 권장드립니다.)
   ```bash
   pip install -r requirements.txt

3. **환경 변수 설정**
   ```bash
   NAVER_ID=your_client_id
   NAVER_PW=pour_client_secret
4. **파이프라인 실행**
   ```bash
   python main.py

전체흐름 : 크롤링 ➡️ 전처리 ➡️ 감성분석 ➡️ 워드클라우드 생성 ➡️ 결과 저장 
