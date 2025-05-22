from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# ===== 검색 키워드 =====
keywords = ["이재명", "김문수", "이준석"]

# ===== 크롬 옵션 설정 (우분투 최적화) =====
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 필요시 주석 해제
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# ===== 드라이버 실행 =====
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# ===== sessionid 기반 로그인 =====
driver.get("https://www.instagram.com/")
sessionid = "31752966551%3AbIEPMQ0s2pAn4y%3A22%3AAYd52xJ6Z61Y8Cr-oTym88q_ogy93kVKF8D7DQmtNQ"  # 본인의 sessionid로 대체
driver.add_cookie({
    "name": "sessionid",
    "value": sessionid,
    "domain": ".instagram.com",
    "path": "/"
})
driver.get("https://www.instagram.com/")
time.sleep(5)

# ===== 크롤링 시작 =====
results = []

for keyword in keywords:
    print(f"\n===== 검색어: {keyword} =====")
    driver.get(f"https://www.instagram.com/explore/tags/{keyword}/")
    time.sleep(5)

    try:
        posts = driver.find_elements(By.CLASS_NAME, "_aagw")
        if not posts:
            print("게시물이 없습니다.")
            continue

        posts[0].click()
        time.sleep(3)

        comment_count_for_keyword = 0
        collected_comments = set()

        while comment_count_for_keyword < 5000:
            try:
                # ===== 댓글 더 보기 반복 클릭 =====
                while True:
                    try:
                        load_more_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="댓글 더 읽어들이기"]')
                        load_more_btn.click()
                        time.sleep(1)
                    except:
                        break  # 더 이상 버튼 없음

                # ===== 댓글 본문만 추출 =====
                comment_elements = driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')
                for ce in comment_elements:
                    comment_text = ce.text.strip()
                    if comment_text and comment_text not in collected_comments:
                        collected_comments.add(comment_text)
                        results.append({
                            "platform": "인스타그램",
                            "press": None,
                            "keyword": keyword,
                            "comment": comment_text
                        })
                        comment_count_for_keyword += 1
                        print(f"[댓글 수집] ({comment_count_for_keyword}) {comment_text}")  # ✅ 로그 출력
                        if comment_count_for_keyword >= 5000:
                            break

                # ===== 다음 게시물로 이동 =====
                try:
                    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aaqg._aaqh")))
                    next_btn.click()
                    time.sleep(2)
                except:
                    print("🚫 다음 게시물이 없습니다.")
                    break

            except Exception as e:
                print(f"[오류] 댓글 처리 중 문제 발생: {e}")
                break

        print(f"🔹 [{keyword}] 댓글 수집 완료: {comment_count_for_keyword}개")

    except Exception as e:
        print(f"[오류] 키워드 처리 실패: {e}")
        continue

# ===== JSON 저장 =====
filename = f"instagram_comments_{time.strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✅ 전체 수집 완료 및 저장: {filename}")
driver.quit()
