
import time
from Insta_gram.crawl.insta import InstagramCrawler

def main():
    sessionid = "YOUR_SESSION_ID"  # 본인의 sessionid 입력
    keywords = ["이재명", "김문수", "이준석"]

    crawler = InstagramCrawler(sessionid=sessionid, keywords=keywords, headless=False)
    crawler.login_with_sessionid()
    crawler.crawl_comments()
    
    filename = f"instagram_comments_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    crawler.save_to_csv(filename)
    crawler.quit()

if __name__ == "__main__":
    main()
