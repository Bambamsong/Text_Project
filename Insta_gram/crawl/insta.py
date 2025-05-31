from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

class InstagramCrawler:
    def __init__(self, sessionid, keywords, headless=False, max_comments=5000):
        self.sessionid = sessionid
        self.keywords = keywords
        self.max_comments = max_comments
        self.driver = self._setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 15)
        self.results = []

    def _setup_driver(self, headless):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login_with_sessionid(self):
        self.driver.get("https://www.instagram.com/")
        self.driver.add_cookie({
            "name": "sessionid",
            "value": self.sessionid,
            "domain": ".instagram.com",
            "path": "/"
        })
        self.driver.get("https://www.instagram.com/")
        time.sleep(5)

    def crawl_comments(self):
        for keyword in self.keywords:
            print(f"\n===== 검색어: {keyword} =====")
            self.driver.get(f"https://www.instagram.com/explore/tags/{keyword}/")
            time.sleep(5)

            try:
                posts = self.driver.find_elements(By.CLASS_NAME, "_aagw")
                if not posts:
                    print("게시물이 없습니다.")
                    continue

                posts[0].click()
                time.sleep(3)

                comment_count = 0
                collected_comments = set()

                while comment_count < self.max_comments:
                    try:
                        while True:
                            try:
                                load_more_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="댓글 더 읽어들이기"]')
                                load_more_btn.click()
                                time.sleep(1)
                            except:
                                break

                        comment_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')
                        for ce in comment_elements:
                            comment_text = ce.text.strip()
                            if comment_text and comment_text not in collected_comments:
                                collected_comments.add(comment_text)
                                self.results.append({
                                    "platform": "인스타그램",
                                    "press": None,
                                    "keyword": keyword,
                                    "comment": comment_text
                                })
                                comment_count += 1
                                print(f"[댓글 수집] ({comment_count}) {comment_text}")
                                if comment_count >= self.max_comments:
                                    break

                        try:
                            next_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aaqg._aaqh")))
                            next_btn.click()
                            time.sleep(2)
                        except:
                            print("다음 게시물이 없습니다.")
                            break

                    except Exception as e:
                        print(f"[오류] 댓글 처리 중 문제 발생: {e}")
                        break

                print(f"🔹 [{keyword}] 댓글 수집 완료: {comment_count}개")

            except Exception as e:
                print(f"[오류] 키워드 처리 실패: {e}")
                continue

    def save_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["platform", "press", "keyword", "comment"])
            writer.writeheader()
            writer.writerows(self.results)
        print(f"\nCSV 저장 완료: {filename}")

    def quit(self):
        self.driver.quit()